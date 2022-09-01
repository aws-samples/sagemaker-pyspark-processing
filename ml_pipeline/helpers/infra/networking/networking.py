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

Description: Helper functions to handler networking configuration
"""
from sagemaker.network import NetworkConfig


def get_network_configuration(subnets, security_group_ids):
    """
    Get the network configuration input object
    Args:
        subnets (list): list of submets to use
        security_group_ids (list): list of segurity group ids to use
    Returns:
        (sagemaker.network.NetworkConfig): network configuration
    """
    return NetworkConfig(
        encrypt_inter_container_traffic=True,
        security_group_ids=security_group_ids,
        subnets=subnets
    )


def get_vpc_configuration(subnet_ids, security_group_ids):
    """
    Helper function that returns the VPC configuration as a dict
    Args:
        subnet_ids (list[str]): list of subnet ids
        security_group_ids (list[str]): list of security group ids

    Returns:
        (dict): VPC configuration
    """
    return {
        "Subnets": subnet_ids,
        "SecurityGroupIds": security_group_ids
    }
