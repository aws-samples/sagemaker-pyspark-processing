"""
 Copyright 2021 Amazon Web Services, Inc. or its affiliates. All Rights Reserved.
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at
     http://www.apache.org/licenses/LICENSE-2.0
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.

Author:  Maira Ladeira Tanke (mttanke@amazon.com)
Author:  Maren Suilmann (suilm@amazon.com)
Author:  Donald Fossouo (fossod@amazon.com)
Author:  Pauline Ting (tingpaul@amazon.com)

Description: SagaMaker Pipeline with PySpark Processor
"""

# import code requirements
# standard libraries import
import logging
import json

# sagemaker model import
import sagemaker
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.pipeline_experiment_config import PipelineExperimentConfig
from sagemaker.workflow.steps import CacheConfig
from sagemaker.processing import ProcessingInput
from sagemaker.workflow.steps import ProcessingStep

from helpers.pipeline.steps.processing.processing_job import create_pyspark_processor
from helpers.infra.networking.networking import get_network_configuration
from helpers.infra.tags.tags import get_tags_input
from helpers.pipeline_utils import get_pipeline_config


def create_pipeline(pipeline_params, logger):
    """
    Args:
        pipeline_params (ml_pipeline.params.pipeline_params.py.Params): pipeline parameters
        logger (logger): logger
    Returns:
        ()
    """
    # Create SageMaker Session
    sagemaker_session = sagemaker.Session()

    # Get Tags
    tags_input = get_tags_input(pipeline_params["tags"])

    # get network configuration
    network_config = get_network_configuration(
        subnets=pipeline_params["network_subnet_ids"],
        security_group_ids=pipeline_params["network_security_group_ids"]
    )

    # Get Pipeline Configurations
    pipeline_config = get_pipeline_config(pipeline_params)

    # setting processing cache obj
    logger.info("Setting " + pipeline_params["pyspark_process_name"]  + " cache configuration 3to 30 days")
    cache_config = CacheConfig(enable_caching=True, expire_after="p30d")

    # processing input arguments. To add new arguments to this list you need to provide two entrances:
    # 1st is the argument name preceded by "--" and the 2nd is the argument value
    # setting up processing arguments
    process_args = [
        "--input_table", pipeline_params["pyspark_process_data_input"].format(pipeline_params["data_bucket"]),
        "--output_table", pipeline_params["pyspark_process_data_output"].format(pipeline_params["data_bucket"])
    ]

    # setting process code
    process_code = "s3://{}/{}/{}".format(
        pipeline_params["infra_bucket"],
        pipeline_params["processing_key"],
        pipeline_params["pyspark_process_code"]
    )

    # setting process support python files
    process_helpers = [
        "s3://{}/{}/{}".format(
            pipeline_params["infra_bucket"],
            pipeline_params["helper_key"],
            pipeline_params["data_utils_code"]
        )
    ]

    # setting pre-process spark configuration files
    process_spark_config_loc = "s3://{}/{}/{}".format(
        pipeline_params["infra_bucket"],
        pipeline_params["spark_key"],
        pipeline_params["spark_config"]
    )

    # setting pre-process spark ui log s3 output location
    process_spark_ui_log_output = "s3://{}/spark_ui_logs/{}".format(
        pipeline_params["data_bucket"],
        pipeline_params["trial"]
    )

    # Create PySpark Processing Step
    logger.info("Creating " + pipeline_params["pyspark_process_name"] + " processor")

    processing_pyspark_processor, processing_run_dependencies = create_pyspark_processor(
        base_job_name=pipeline_params["pyspark_process_name"],
        framework_version=pipeline_params["pyspark_framework_version"],
        job_code_uri=process_code,
        job_helpers_uris=process_helpers,
        job_args=process_args,
        sagemaker_session=sagemaker_session,
        network_config_input=network_config,
        tags_input=tags_input,
        processing_instance_type=pipeline_params["pyspark_process_instance_type"],
        processing_instance_count=pipeline_params["pyspark_process_instance_count"],
        role=pipeline_params["pipeline_role"],
        spark_event_logs_s3_uri=process_spark_ui_log_output,
        volume_kms_key=pipeline_params["pyspark_process_volume_kms"],
        output_kms_key=pipeline_params["pyspark_process_output_kms"]
    )
    inputs = [
        ProcessingInput(
            source=process_spark_config_loc,
            destination="/opt/ml/processing/input/conf",
            s3_data_type="S3Prefix",
            s3_input_mode="File",
            s3_data_distribution_type="FullyReplicated",
            s3_compression_type="None"
        )
    ]
    # create step
    pyspark_processing_step = ProcessingStep(
        name=pipeline_params["pyspark_process_name"],
        processor=processing_pyspark_processor,
        job_arguments=processing_run_dependencies.arguments,
        code=processing_run_dependencies.code,
        cache_config=cache_config,
        inputs=inputs,
        outputs=processing_run_dependencies.outputs
    )

    # Create Pipeline
    pipeline = Pipeline(
        name=pipeline_params["pipeline_name"],
        steps=[
            pyspark_processing_step
        ],
        pipeline_experiment_config=PipelineExperimentConfig(
            pipeline_params["pipeline_name"],
            pipeline_config["trial"]
        ),
        sagemaker_session=sagemaker_session
    )
    pipeline.upsert(
        role_arn=pipeline_params["pipeline_role"],
        description="Example pipeline",
        tags=tags_input
    )
    return pipeline


def main():
    # set up logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.info("Get Pipeline Parameter")

    with open("ml_pipeline/params/pipeline_params.json", "r") as f:
        pipeline_params = json.load(f)
    print(pipeline_params)

    logger.info("Create Pipeline")
    pipeline = create_pipeline(pipeline_params, logger=logger)
    logger.info("Execute Pipeline")
    execution = pipeline.start()
    return execution


if __name__ == "__main__":
    main()
