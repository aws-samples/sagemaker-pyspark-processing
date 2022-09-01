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

Description: Tests for ml_pipeline.helpers.pipeline.step.training.training_job.py
"""
from ml_pipeline.helpers.pipeline.steps.training.training_job import create_estimator


def test_create_estimator_returns_expected_objects():
    estimator = create_estimator(
        estimator_name="estimator_test",
        estimator_entry_point="test_entry_point",
        estimator_code_dir="entry_point_dir",
        role="role_arn",
        instance_type="type1",
        instance_count=1
    )

    assert estimator.entry_point == "test_entry_point"
    assert estimator.source_dir == "entry_point_dir"