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

Description: Tests for ml_pipeline.helpers.pipeline.step.processing.processing_job.py
"""
from ml_pipeline.helpers.pipeline.steps.processing.processing_job import (
    create_script_processor,
    create_pyspark_processor
)


def test_create_pyspark_processor_returns_expected_objects():
    processor, run_args = create_pyspark_processor(
        base_job_name="test_job",
        framework_version="2.0",
        job_code_uri="s3://job_uri",
        role="role_arn",
        processing_instance_type="type1",
        processing_instance_count=6
    )

    assert processor.base_job_name == "test_job"
    assert processor.framework_version == "2.0"
    assert processor.job_code_uri == "s3://job_uri"
    assert processor.role == "role_arn"
    assert processor.processing_instance_type == "type1"
    assert processor.processing_instance_count == 6


def test_create_script_processor_returns_expected_objects():
    processor, run_args = create_script_processor(
        base_job_name="test_job",
        job_code_uri="s3://job_code_uri",
        image_uri="image_uri",
        role="role",
        command=["python3"],
        processing_instance_type="type1",
        processing_instance_count=1
    )

    assert processor.base_job_name == "test_job"
    assert processor.job_code_uri == "s3://job_uri"
    assert processor.image_uri == "image_uri"
    assert processor.role == "role_arn"
    assert processor.command == ["python3"]
    assert processor.processing_instance_type == "type1"
    assert processor.processing_instance_count == 6
