#!/bin/bash
set -e # exit script if any command fails

# installing sagemaker to run code locally 
pip install zip-files==0.4.1 sagemaker==2.78.0 matplotlib==3.5.2 sklearn==0.0 protobuf==3.19.0
pip install -U sagemaker
# Allow execution of this script from any location
echo "Current directory:"
pwd

# Variable with script path 
SCRIPTDIR="$(dirname "$0")"
echo "Path of script:"
echo $SCRIPTDIR
cd $SCRIPTDIR

# # create tar file 
# cd ../../src/model
# tar -zcvf model_code.tar.gz  entry_point.py model_train.py model_predict.py model_utils.py
# # move tar file to run-pipelines-locally folder 
# mv model_code.tar.gz ../../ml_pipeline/run_pipelines_locally/model_code.tar.gz
# # update tar file to s3
# cd ../../ml_pipeline/run_pipelines_locally/
# # saving model_code versioned for auditability
# aws s3 cp model_code.tar.gz s3://path to/model_code.tar.gz

# move to root folder 
cd ../../
# sync src folder 
# saving src versioned for auditability
aws s3 sync src s3://example-infra-bucket-pyspark-blogpost/src --region eu-west-1
# sync ml_pipeline folder
aws s3 sync ml_pipeline s3://example-infra-bucket-pyspark-blogpost/ml_pipeline --region eu-west-1

# run 
python ml_pipeline/pipeline.py

