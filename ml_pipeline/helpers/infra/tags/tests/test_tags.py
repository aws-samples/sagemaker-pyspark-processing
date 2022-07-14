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

Description: Tests for ml_pipeline.helpers.infra.tags.tags.py
"""
from ml_pipeline.helpers.infra.tags.tags import get_tags_input


def test_get_tags_input_expected_objects():
    tags = get_tags_input(
        tags={
            "tag1": "tag1_val",
            "tag2": "tag2_val"
        }
    )

    assert tags == [
        {"Key": "tag1", "Value": "tag1_val"},
        {"Key": "tag2", "Value": "tag2_val"}
    ]
