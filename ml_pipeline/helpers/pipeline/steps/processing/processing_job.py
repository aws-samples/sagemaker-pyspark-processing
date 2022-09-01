"""
 Copyright 2021 Amazon Web Services, Inc. or its affiliates. All Rights Reserved.
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at https://www.apache.org/licenses/LICENSE-2.0
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.

Description: Helper functions to handle SageMaker Processing Jobs
"""

from sagemaker.spark.processing import PySparkProcessor
from sagemaker.processing import ScriptProcessor


def create_pyspark_processor(base_job_name, framework_version, job_code_uri, role, processing_instance_type,
                             processing_instance_count=1, job_helpers_uris=None, job_args=None,
                             sagemaker_session=None, network_config_input=None, tags_input=None, volume_kms_key=None,
                             output_kms_key=None, spark_event_logs_s3_uri=None):
    """
    function that creates a pyspark processing job and its running dependencies
    Args:
        base_job_name (srt): prefix for the processing name
        framework_version (str): the version of SageMaker PySpark
        job_code_uri (str): path (local or s3) to a python file to submit to spark as the primary application.
                            This translates to the code property on the returned RunArgs object.
        role (str): An AWS IAM role name or ARN.
        processing_instance_type (str): Type of EC2 instance to use for processing, for example, ‘ml.c4.xlarge’.
        processing_instance_count (int): The number of instances to run the Processing job with. Defaults to 1.
        job_helpers_uris (list[str]): list of paths (local or s3) to provide for the spark-submit -py-files option
                                      on the returned RunArgs object. Default: None
        job_args (list(str)): list of string arguments to be passed to a processing job. Default: None
        sagemaker_session(sagemaker.session.Session): Session object which manages interactions with Amazon SageMaker
                                                      APIs and any other AWS services needed. If not specified, the
                                                      processor creates one using the default AWS configuration chain.
        network_config_input(sagemaker.network.NetworkConfig): A NetworkConfig object that configures network isolation,
                                                              encryption of inter-container traffic, security group IDs,
                                                              and subnets.
        tags_input (list[dict]): List of tags to be passed to the processing job. Default: None
        volume_kms_key (str): A KMS key for the processing volume.
        output_kms_key(str): The KMS key id for all ProcessingOutputs.
        spark_event_logs_s3_uri (str):  S3 path where spark application events will be published to.
    Returns:
        sagemaker.spark.processing.PySparkProcessor: The SageMaker Processing Job
        sagemaker.processing.RunArgs: parameters that correspond to the Processor Job
    """
    # setting up spark processor
    spark_processor = PySparkProcessor(
        base_job_name=base_job_name,
        framework_version=framework_version,
        role=role,
        instance_count=processing_instance_count,
        instance_type=processing_instance_type,
        volume_kms_key=volume_kms_key,
        output_kms_key=output_kms_key,
        network_config=network_config_input,
        tags=tags_input,
        sagemaker_session=sagemaker_session
    )
    # setting up dependencies
    print("job_code_uri:", job_code_uri)
    print("job_helpers_uris:", job_helpers_uris)
    print("job_args:", job_args)
    print("spark_event_logs_s3_uri:", spark_event_logs_s3_uri)
    run_ags_dependencies = spark_processor.get_run_args(
        submit_app=job_code_uri,
        submit_py_files=job_helpers_uris,
        arguments=job_args,
        spark_event_logs_s3_uri=spark_event_logs_s3_uri
    )
    return spark_processor, run_ags_dependencies


def create_script_processor(base_job_name, job_code_uri, image_uri, role, command, processing_instance_type,
                            processing_instance_count=1, job_args=None, sagemaker_session=None,
                            network_config_input=None, tags_input=None, volume_kms_key=None, output_kms_key=None):
    """
    function that creates a script processing job and its running dependencies
    Args:
        base_job_name (srt): prefix for the processing name
        image_uri (str): The URI of the Docker image to use for the processing jobs.
        job_code_uri (str): path (local or s3) to a python file to submit to spark as the primary application.
                            This translates to the code property on the returned RunArgs object.
        role (str): An AWS IAM role name or ARN.
        command (list[str]): The command to run, along with any command-line flags. Example: [“python3”, “-v”].
        processing_instance_type (str): Type of EC2 instance to use for processing, for example, ‘ml.c4.xlarge’.
        processing_instance_count (int): The number of instances to run the Processing job with. Defaults to 1.
        job_args (list(str)): list of string arguments to be passed to a processing job. Default: None
        sagemaker_session(sagemaker.session.Session): Session object which manages interactions with Amazon SageMaker
                                                      APIs and any other AWS services needed. If not specified, the
                                                      processor creates one using the default AWS configuration chain.
        network_config_input(sagemaker.network.NetworkConfig): A NetworkConfig object that configures network isolation,
                                                              encryption of inter-container traffic, security group IDs,
                                                              and subnets.
        tags_input (list[dict]): List of tags to be passed to the processing job. Default: None
        volume_kms_key (str): A KMS key for the processing volume.
        output_kms_key(str): The KMS key id for all ProcessingOutputs.
    Returns:
        sagemaker.processing.ScriptProcessor: The SageMaker Processing Job
        sagemaker.processing.RunArgs: parameters that correspond to the Processor Job
    """
    # setting up script processor
    script_processor = ScriptProcessor(
        base_job_name=base_job_name,
        image_uri=image_uri,
        role=role,
        instance_count=processing_instance_count,
        instance_type=processing_instance_type,
        volume_kms_key=volume_kms_key,
        output_kms_key=output_kms_key,
        network_config=network_config_input,
        tags=tags_input,
        sagemaker_session=sagemaker_session,
        command=command
    )
    run_ags_dependencies = script_processor.get_run_args(
         code=job_code_uri,
         arguments=job_args,
    )
    return script_processor, run_ags_dependencies
