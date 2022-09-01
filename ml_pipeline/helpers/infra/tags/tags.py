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

Description: Helper functions to handle tags
"""


def get_tags_input(tags):
    """
    Get the tags input object as a list of dictionary from a dictionary of tags in the format
    {
        tag1: tag_value1,
        tag2: tag_value2,
        ...
        tagN: tag_valueN
    }
    Args:
        tags (dict): dictionary of tags

    Returns:
        (list[dict]): list of dictionaries of format {"Key": tag, "Value": tag_value}
    """
    return [{"Key": tag, "Value": tags[tag]} for tag in tags]
