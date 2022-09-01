#!/bin/bash
set -e # exit script if any command fails

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
aws s3 sync src s3://<INFRA_S3_BUCKET>/src --region eu-west-1
# sync ml_pipeline folder
aws s3 sync ml_pipeline s3://<INFRA_S3_BUCKET>/ml_pipeline --region eu-west-1

# run 
python ml_pipeline/pipeline.py

