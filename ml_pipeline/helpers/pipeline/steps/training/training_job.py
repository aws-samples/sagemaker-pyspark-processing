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

Description: Helper functions to handle SageMaker Training Jobs
"""
from sagemaker.sklearn import SKLearn
from sagemaker.mxnet import MXNet
from sagemaker.pytorch import PyTorch
from sagemaker.tensorflow import TensorFlow
from sagemaker.xgboost import XGBoost


def create_estimator(estimator_name, estimator_entry_point, estimator_code_dir, role, instance_type, instance_count=1,
                     framework_version="0.20.0", tags=None, subnets=None, security_group_ids=None,
                     use_spot_instances=True, sagemaker_session=None, metric_definitions=None,
                     enable_sagemaker_metrics=False, hyperparameters=None, estimator_type="sklearn"):
    """
    Create an estimator object for the model
    Technical documentation on preparing training scripts for SageMaker is available on the project home-page:
        https://github.com/aws/sagemaker-python-sdk
    Args:
        estimator_name (str): prefix for the training name
        estimator_entry_point (str): Path (absolute or relative) to the Python source file which should be executed as
                                     the entry point to training. The entry_point must point to a file located at the
                                     root of source_dir.
        estimator_code_dir (str): Path (absolute, relative or an S3 URI) to a directory with any other training source
                                  code dependencies aside from the entry point file (default: None). If source_dir is
                                  an S3 URI, it must point to a tar.gz file. Structure within this directory are
                                  preserved when training on Amazon SageMaker.
        role (str): An AWS IAM role name or ARN.
        instance_type (str): Type of EC2 instance to use for training, for example, ‘ml.c4.xlarge’.
        instance_count (int):The number of instances to run the training job with. Defaults to 1.
        framework_version (str): Scikit-learn version you want to use for executing your model training code.
                                 List of supported versions:
                                     https://github.com/aws/sagemaker-python-sdk#sklearn-sagemaker-estimators
                                Default value: 0.20.0
        tags (list[dict]): List of tags to be passed to the processing job. Default: None
        subnets (list[str]): List of subnet ids. If not specified training job will be created without VPC config.
        security_group_ids (list[str]): List of security group ids. If not specified training job will be created without VPC config.
        use_spot_instances (bool):
        sagemaker_session(sagemaker.session.Session): Session object which manages interactions with Amazon SageMaker
                                                      APIs and any other AWS services needed. If not specified, the
                                                      processor creates one using the default AWS configuration chain.
        metric_definitions (list[dict]): A list of dictionaries that defines the metric(s) used to evaluate the training
                                         jobs. Each dictionary contains two keys: 'Name' for the name of the metric,
                                         and 'Regex' for the regular expression used to extract the metric from the logs.
                                         This should be defined only for jobs that don't use an Amazon algorithm.
        enable_sagemaker_metrics (bool): enable SageMaker Metrics Time Series. For more information, see
                                         `AlgorithmSpecification API
                                         <https://docs.aws.amazon.com/sagemaker/latest/dg/API_AlgorithmSpecification.html#SageMaker-Type-AlgorithmSpecification-EnableSageMakerMetricsTimeSeries>`_.
                                        (default: None).
        hyperparameters (dict): Hyperparameters that will be used for training (default: None). The hyperparameters are
                                made accessible as a dict[str, str] to the training code on SageMaker. For convenience,
                                this accepts other types for keys and values, but str() will be called to convert them
                                before training.
        estimator_type (str): type of estimator. Available values: ["sklearn", "mxnet", "pytorch", "tensorflow",
                              "xgboost"]. Default "sklearn"

    Returns:

    """
    # create a sklearn model. For more information:
    # https://sagemaker.readthedocs.io/en/stable/frameworks/sklearn/using_sklearn.html
    if estimator_type == "sklearn":
        estimator = SKLearn(
            base_job_name=estimator_name,
            entry_point=estimator_entry_point,
            source_dir=estimator_code_dir,
            role=role,
            instance_type=instance_type,
            instance_count=instance_count,
            framework_version=framework_version,
            tags=tags,
            subnets=subnets,
            security_group_ids=security_group_ids,
            encrypt_inter_container_traffic=True,
            use_spot_instances=use_spot_instances,
            sagemaker_session=sagemaker_session,
            metric_definitions=metric_definitions,
            enable_sagemaker_metrics=enable_sagemaker_metrics,
            hyperparameters=hyperparameters
        )
    elif estimator_type == "mxnet":
        estimator = MXNet(
            base_job_name=estimator_name,
            entry_point=estimator_entry_point,
            source_dir=estimator_code_dir,
            role=role,
            instance_type=instance_type,
            instance_count=instance_count,
            framework_version=framework_version,
            tags=tags,
            subnets=subnets,
            security_group_ids=security_group_ids,
            encrypt_inter_container_traffic=True,
            use_spot_instances=use_spot_instances,
            sagemaker_session=sagemaker_session,
            metric_definitions=metric_definitions,
            enable_sagemaker_metrics=enable_sagemaker_metrics,
            hyperparameters=hyperparameters
        )
    elif estimator_type == "pytorch":
        estimator = PyTorch(
            base_job_name=estimator_name,
            entry_point=estimator_entry_point,
            source_dir=estimator_code_dir,
            role=role,
            instance_type=instance_type,
            instance_count=instance_count,
            framework_version=framework_version,
            tags=tags,
            subnets=subnets,
            security_group_ids=security_group_ids,
            encrypt_inter_container_traffic=True,
            use_spot_instances=use_spot_instances,
            sagemaker_session=sagemaker_session,
            metric_definitions=metric_definitions,
            enable_sagemaker_metrics=enable_sagemaker_metrics,
            hyperparameters=hyperparameters
        )
    elif estimator_type == "tensorflow":
        estimator = TensorFlow(
            base_job_name=estimator_name,
            entry_point=estimator_entry_point,
            source_dir=estimator_code_dir,
            role=role,
            instance_type=instance_type,
            instance_count=instance_count,
            framework_version=framework_version,
            tags=tags,
            subnets=subnets,
            security_group_ids=security_group_ids,
            encrypt_inter_container_traffic=True,
            use_spot_instances=use_spot_instances,
            sagemaker_session=sagemaker_session,
            metric_definitions=metric_definitions,
            enable_sagemaker_metrics=enable_sagemaker_metrics,
            hyperparameters=hyperparameters
        )
    elif estimator_type == "xgboost":
        estimator = XGBoost(
            base_job_name=estimator_name,
            entry_point=estimator_entry_point,
            source_dir=estimator_code_dir,
            role=role,
            instance_type=instance_type,
            instance_count=instance_count,
            framework_version=framework_version,
            tags=tags,
            subnets=subnets,
            security_group_ids=security_group_ids,
            encrypt_inter_container_traffic=True,
            use_spot_instances=use_spot_instances,
            sagemaker_session=sagemaker_session,
            metric_definitions=metric_definitions,
            enable_sagemaker_metrics=enable_sagemaker_metrics,
            hyperparameters=hyperparameters
        )
    else:
        supported_values = '["sklearn", "mxnet", "pytorch", "tensorflow", "xgboost"]'
        raise ValueError("Invalid estimator type. Supported values: " + supported_values)
    return estimator
