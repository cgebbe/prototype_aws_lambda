# About

This is a prototype of how to deploy a model as an application on AWS with a REST API. The diagram below (by me) depicts how the application could fit in a larger system.

![cloud architecture](cloud_architecture.png)

## Problem (hypothetical)

Given a model prototype in the form of a Juypter notebook, _productionize_ it. This means adding a CI pipeline with tests and deploying the model with a REST API.

## Solution

- Split the existing code in the Jupyter notebook into python files (most importantly `train.py` and `predict.py`)
- Add tests and linting
- Package the code in a Docker container. Use a [base image from AWS lambda](https://docs.aws.amazon.com/lambda/latest/dg/runtimes-images.html#runtimes-images-lp) since it already includes the required runtime library for interfacing with AWS lambda.
- Wrap the prediction code in `app.py` for receiving a JSON-formatted event by AWS lambda. The container can now be tested locally using `curl` (see below).
- In AWS, upload your container, setup the AWS lambda function and a REST API.

# How to use

## Use container locally

```bash
# build docker image
IMAGE_NAME="aws_inference_image"
docker build -t $IMAGE_NAME .

# test docker locally
CONTAINER_NAME="aws_inference_container"
docker stop $CONTAINER_NAME
docker rm $CONTAINER_NAME
docker run -d -p 9000:8080 --name $CONTAINER_NAME $IMAGE_NAME
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{ "sensor_1": "[1,2.0,3]", "sensor_2": "[1,-1,0]" }'
# should return {"class": [0.0, 1.0, 1.0]}
```

## Use deployed container on AWS Lambda

```bash
curl -v -X POST \
  'https://l5q3tq5jxk.execute-api.eu-central-1.amazonaws.com/test/zeiss_cg' \
  -H 'content-type: application/json' \
  -d '{ "sensor_1": "[1,2.0,3]", "sensor_2": "[1,-1,0]" }'
# should return {"class": [0.0, 1.0, 1.0]}
```

# How to run CI

```bash
# start the docker container (using parameter from above!)
docker run --rm -it --entrypoint="bash" $IMAGE_NAME
make check
```

# Remarks

This code still contains _several_ inaccuracies:

- Lint: No pylint, flake8, prettier, few type annotations
- Hack to run pytest by placing conftest.py in root directory
- no CLI interface (except for `app.py`)
- Docker image is bloated from test dependencies and no-cache
- Full code is copied to docker (although test are not needed...)
- ...
