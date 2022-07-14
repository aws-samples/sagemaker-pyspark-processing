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

Author:  Maira Ladeira Tanke (mttanke@amazon.com)
Author:  Maren Suilmann (suilm@amazon.com)
Author:  Donald Fossouo (fossod@amazon.com)
Author:  Pauline Ting (tingpaul@amazon.com)

Description: Support functions for SageMaker Training pipeline
"""
from datetime import datetime


def get_pipeline_config(params):
    """
    Get pipeline configuration and step names
    Args:
        params (ml_pipeline.params.pipeline_params.py.Params): parameters
    Returns:
         (dict): step names and trial name
    """
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")

    pipeline_config = {
        "trial": params["pipeline_name"] + "-" + dt_string,
        "pre-processing-step": "pre-processing",
        "model-step": "model"
    }
    return pipeline_config


