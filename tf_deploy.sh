#!/bin/bash
cd lambdas; zip -r ../dist/lambda.zip *; cd ..;
terraform -chdir=infra apply -var-file=.tfvars