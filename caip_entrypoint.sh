#!/usr/bin/env bash
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/tensorrtserver/lib

echo "Running: triton server and listener."

trtserver --model-repository=${MODEL_DIR} &
python3 listener.py $@

