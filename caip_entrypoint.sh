#!/usr/bin/env bash
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/tensorrtserver/lib

echo "Running: triton server and listener."

trtserver --model-repository=${AIP_STORAGE_URI} &
python3 listener.py $@

