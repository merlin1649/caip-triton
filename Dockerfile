# Copyright (c) 2020, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM nvcr.io/nvidia/tritonserver:20.03-py3

RUN apt update && \
    mkdir /opt/tensorrtserver/triton_client && cd /opt/tensorrtserver/triton_client && \
    wget https://github.com/NVIDIA/triton-inference-server/releases/download/v1.12.0/v1.12.0_ubuntu1804.clients.tar.gz && \
    tar -zxvf v1.12.0_ubuntu1804.clients.tar.gz && \
    pip3 install --upgrade pip && \
    pip3 install flask Pillow requests && \
    pip3 install /opt/tensorrtserver/triton_client/python/*.whl

WORKDIR /opt/tensorrtserver/

COPY listener4.py /opt/tensorrtserver/listener.py
COPY caip_entrypoint.sh /opt/tensorrtserver/
COPY grpc_gcp_caip_pb2.py /opt/tensorrtserver/

ENTRYPOINT ["bash", "caip_entrypoint.sh"]
