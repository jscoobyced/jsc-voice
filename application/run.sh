#!/bin/bash

source .venv/bin/activate
python server.py > ./application.log 2> ./error.log 