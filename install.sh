#!/bin/bash

echo Beginning installation
# python3 -m venv venv
# Cleanup of any previous install
echo Cleaning up old installations
rm -f jsonFormat_pb2*
rm -rf logs

echo Creating ./logs folder and ./logs/pip.log file
mkdir logs
touch logs/pip.log

pip3 install grpcio grpcio-tools chess > logs/pip.log
cd src
python3 -m grpc_tools.protoc -I ../proto --python_out=. --grpc_python_out=. ../proto/jsonFormat.proto