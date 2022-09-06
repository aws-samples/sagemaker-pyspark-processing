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

Description: Tests for ml_pipeline.helpers.infra.networking.networking.py
"""
from ml_pipeline.helpers.infra.networking.networking import get_network_configuration, get_vpc_configuration


def test_get_network_configuration_expected_objects():
    net_config = get_network_configuration(
        subnets=["subnet1", "subnet2"],
        security_group_ids=["sg1", "sg2"]
    )

    assert net_config.subnets == ["subnet1", "subnet2"]
    assert net_config.security_group_ids == ["sg1", "sg2"]


def test_get_vpc_configuration_returns_expected_objects():
    vpc_config = get_vpc_configuration(
        subnet_ids=["subnet1", "subnet2"],
        security_group_ids=["sg1", "sg2"]
    )

    assert vpc_config["Subnets"] == ["subnet1", "subnet2"]
    assert vpc_config["SecurityGroupIds"] == ["sg1", "sg2"]
