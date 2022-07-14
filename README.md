# Secure PySpark Pipeline example

This repository contains an Amazon SageMaker Pipeline structure to run a 
PySpark job inside a SageMaker Processing Job running inside a VPC with 
encryption enabled. It also enables the creation of a Spark UI from the pyspark 
logs generated by the execution.

## Solution Architecture
TODO

## Solution Deployment
###  Pre-requisites
This repo assumes it will be executed inside SageMaker Studio. 
To do so, you need to clone this repository in your SageMaker Studio deployment.

This repo also assumes that the VPC configuration is already available on your AWS account.
To configure the code for your VPC configuration, you need to edit the `ml_pipeline/params/pipeline_params.json` file.

### Repository Structure
```
.
├── .gitignore
├── poetry.lock
├── pyproject.toml
├── README.md
├── requirements.txt
├── ml_pipeline                                 <--- code to generate your Amazon SageMaker Pipelines
│   ├── helpers                                 <--- support funtions to help you create your pipeline
│   │   ├── infra                               <--- Infrastructure related support functions
│   │   │   ├── networking                      <--- networking support functions
│   │   │   └── tags                            <--- tags support functions
│   │   ├── pipeline                            <--- Pipeline steps support function
│   │   │   └── steps                           
│   │   │       ├── processing                  <--- SageMaker Processing Jobs support function
│   │   │       ├── training                    <--- SageMaker Training Jobs support function
│   │   │       ├── transform                   <--- SageMaker Batch Transform Jobs support function
│   │   │       └── others                      <--- Other SageMaker services support functions
│   │   └── pipeline_utils.py                    <--- Pipeline general support functions
│   │── params                                  
│   │   └── pipeline_params.json                <--- Pipeline parameters   
│   └── pipeline.py                             <--- Pipeline creation file                  
├── notebook
│   └── Create_Iris_ParquetFiles.ipynb          <--- Example notebook
└── src                                         <--- Use case code where you develop your data processing and model training functionalities
    ├── helper                                  <--- support functions
    │   └── data_utils.py                       <--- common data processing functions
    ├── processing
    │   └── process_pyspark.py                  <--- PySpark data processing file
    └── spark_configuration
        └── configuration.json                  <--- pyspark configuration json

```

## Running Pipeline

TODO