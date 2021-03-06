#!/usr/bin/env bash

#        usage: sagemaker_deploy.py [-h] [-o OUTPUT] [-e {local,S3}] [-r ROLE] image_uri
#
#    Deploy load forecaster using Sagemaker
#
#    positional arguments:
#      image_uri             URI of the docker image
#
#    optional arguments:
#      -h, --help            show this help message and exit
#      -o OUTPUT, --output OUTPUT
#                            output path directory
#      -e {local,S3}, --environment {local,S3}
#                            run image locally (requires docker) (default) or in S3
#      -r ROLE, --role ROLE  AWS role ARN

python -m sagemaker_deploy load-forecaster \
  -o /Users/markbarna/GitHub/load-forecaster/data/ \
  -e local