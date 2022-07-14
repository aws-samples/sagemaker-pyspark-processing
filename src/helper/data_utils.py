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

Description: Example of data utils file for pyspark processor
             This file presents code examples for:
              * read parquet data from s3
              * set logs to be displayed with the start of the job execution
"""
# standard libraries import
import logging
from pathlib import Path

# aws libraries
import boto3

# pyspark libraries import
from pyspark.sql.functions import input_file_name
import pyspark.sql.functions as f

class Unbuffered(object):
    """
    Class to print logs in real time during job execution
    """
    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def writelines(self, data):
        self.stream.writelines(data)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


def spark_read_parquet(spark, path, logger, merge_schema="true", header="true", add_partition_to_cols=False,
                       partition_col=None, schema=None, date_partition=False, date_format=None):
    """
    Read data from s3 into a pyspark dataframe with relevant logging
    Args:
        spark (SparkSession): PySpark session
        path (str): path where the data is located in s3
        logger (logging): logging obj
        merge_schema (str): string with boolean value to merge multiple parquet
        header (str): string with boolean indicating if header is present on data
        add_partition_to_cols (bool): boolean to indicate if the partition should be added to data as an extra col
        partition_col (str): Name of partition column
        schema (StructType): schema of the parquet file of StructType partitions with different schemas.
                             It supplies null values to any columns missing from the parquet partitions
        date_partition (bool): boolean to indicate if partition column is a date
        date_format (str): date format in case partition column is a date
    Returns:
        (pyspark.DataFrame): spark df with data
    """
    if add_partition_to_cols and (partition_col is None):
        raise ValueError("partition_col must be provided when add_partition_to_cols is True")

    if date_partition and (not add_partition_to_cols):
        raise ValueError("date_partition can only be True with partition should be added to columns "
                         "(add_partition_to_cols = True)")

    if date_partition and (date_format is None):
        raise ValueError("date_format cannot be None if date_partition = True")

    fn_col = "filename"
    if schema:
        df = spark.read \
                  .option("mergeSchema", merge_schema) \
                  .option("header", header) \
                  .schema(schema) \
                  .parquet(path) \
                  .withColumn(fn_col, input_file_name())
    else:
        df = spark.read \
                  .option("mergeSchema", merge_schema) \
                  .option("header", header) \
                  .option("inferSchema", "true") \
                  .parquet(path)\
                  .withColumn(fn_col, input_file_name())
    if add_partition_to_cols:
        # creating the column partition from path partition
        df = df.withColumn(partition_col, f.split(f.col(fn_col), "=").getItem(1)) \
               .drop(fn_col)
        if date_partition:
            df = df.withColumn(partition_col, f.to_timestamp(f.split(f.col(partition_col), "/").getItem(0), date_format))

    logger.info(f"Read data from {path} with schema as: {str(df.columns)}")
    return df


def spark_save_data(df, output_path, output_content_type="text/csv", mode="overwrite", header="true",
                    partition_data=False, partition_col=None):
    """
    Save data using pyspark. This function can save data to s3 and locally using csv or parquet data formats
    Args:
        df (pyspark.sql.DataFrame): PySpark DataFrame with data to save
        output_path (str): path to save data to. Usually an s3 path
        output_content_type (str): output content type. Allowed values: text/csv or application/x-parquet
        mode (str): saving data mode. Allowed values overwrite or append
        header (str): string of boolean to indicate if header should be included on saved data.
                      Allowed values: true or false
        partition_data (bool): boolean to indicate if data should be partitioned
        partition_col (str): column to partition data on. Must be provided if partition_date = True
    """
    if output_content_type not in ["text/csv", "application/x-parquet"]:
        raise TypeError(f"Invalid output_content_type value. Found {output_content_type}. "
                        f"Allowed values: text/csv or application/x-parquet")
    if partition_data:
        if output_content_type == "text/csv":
            df.write.mode(mode).partitionBy(partition_col).format("com.databricks.spark.csv")\
              .option("header", header).save(output_path)

        else:
            df.write.mode(mode).partitionBy(partition_col)\
              .option("header", header).save(output_path)
    else:
        if output_content_type == "text/csv":
            df.write.mode(mode).format("com.databricks.spark.csv").option("header", header).save(output_path)

        else:
            df.write.mode(mode).option("header", header).save(output_path)
