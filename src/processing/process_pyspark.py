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

Description: Example of pre-processing code using a PySpark processor
             This file presents code examples for:
              * read parameters from the processing job
              * read parquet data from s3
              * save data to s3
              * set logs to be displayed with the start of the job execution
              * use extra helper python files
              * Add extra parameters to SageMaker Experiments
"""

# import requirements
import argparse
import logging
import sys
import os
import pandas as pd

# spark imports
from pyspark.sql import SparkSession
from pyspark.sql.functions import (udf, col)
from pyspark.sql.types import StringType, StructField, StructType, FloatType

from data_utils import(
    spark_read_parquet,
    Unbuffered
)

sys.stdout = Unbuffered(sys.stdout)

# Define custom handler
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def main(data_path):

    spark = SparkSession.builder.appName("PySparkJob").getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")

    schema = StructType(
        [
            StructField("sex", StringType(), True),
            StructField("length", FloatType(), True),
            StructField("diameter", FloatType(), True),
            StructField("height", FloatType(), True),
            StructField("whole_weight", FloatType(), True),
            StructField("shucked_weight", FloatType(), True),
            StructField("viscera_weight", FloatType(), True),
            StructField("rings", FloatType(), True),
        ]
    )

    df = spark.read.csv(data_path, header=False, schema=schema)
    return df.select("sex", "length", "diameter", "rings")

if __name__ == "__main__":
    logger.info(f"===============================================================")
    logger.info(f"================= Starting pyspark-processing =================")
    parser = argparse.ArgumentParser(description="app inputs")
    parser.add_argument("--input_table", type=str, help="path to the channel data")
    parser.add_argument("--output_table", type=str, help="path to the output data")
    args = parser.parse_args()
    
    df = main(args.input_table)

    logger.info("Writing transformed data")
    df.write.csv(os.path.join(args.output_table, "transformed.csv"), header=True, mode="overwrite")

    # save data
    df.coalesce(10).write.mode("overwrite").parquet(args.output_table)

    logger.info(f"================== Ending pyspark-processing ==================")
    logger.info(f"===============================================================")
