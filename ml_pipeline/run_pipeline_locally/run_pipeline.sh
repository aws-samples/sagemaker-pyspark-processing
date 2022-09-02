#!/bin/bash
set -e # exit script if any command fails

# TODO: Populate those variables with the Infra and Data buckets names
INFRA_S3_BUCKET="<INFRA_S3_BUCKET>"
DATA_S3_BUCKET="<DATA_S3_BUCKET>"

# installing sagemaker to run code locally 
pip install -r ../../requirements.txt
pip install -U sagemaker
# Allow execution of this script from any location
echo "Current directory:"
pwd

# Variable with script path 
SCRIPTDIR="$(dirname "$0")"
echo "Path of script:"
echo $SCRIPTDIR
cd $SCRIPTDIR

# move to root folder 
cd ../../
# sync src folder 
# saving src versioned for auditability
aws s3 sync src s3://$INFRA_S3_BUCKET/src
# sync ml_pipeline folder
aws s3 sync ml_pipeline s3://$INFRA_S3_BUCKET/ml_pipeline

# copy sample data to S3
aws s3 cp sample_data/abalone_data.csv s3://$DATA_S3_BUCKET/data_input/abalone_data.csv

# run 
python ml_pipeline/pipeline.py

