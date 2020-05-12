#!/usr/bin/env bash

echo "Running: triton server and listener."

trtserver --model-repository=${MODEL_DIR} &
python3 listener.py $@

