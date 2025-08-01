#!/bin/bash

if [ ! -d "chunker-venv" ]; then
    python3 -m venv chunker-venv
fi

source ./chunker-venv/bin/activate
pip install --no-index --find-links=./wheels -r requirements-wheel.txt


