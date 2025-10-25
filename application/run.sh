#!/bin/bash

CURRENT_DIR=$(dirname $0)
cd $CURRENT_DIR
source .venv/bin/activate
python server.py > ./application.log 2> ./error.log 