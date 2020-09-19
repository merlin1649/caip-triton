FROM nvcr.io/nvidia/tritonserver:20.08-py3

RUN apt update && \
    mkdir /opt/tritonserver/triton_client && cd /opt/tritonserver/triton_client && \
    wget https://github.com/NVIDIA/triton-inference-server/releases/download/v1.12.0/v1.12.0_ubuntu1804.clients.tar.gz && \
    tar -zxvf v1.12.0_ubuntu1804.clients.tar.gz && \
    apt-get -y install python3-pip && \
    pip3 install flask Pillow requests && \
    pip3 install /opt/tritonserver/triton_client/python/*.whl

WORKDIR /opt/tensorrtserver/

COPY listener.py /opt/tritonserver/listener.py
COPY caip_entrypoint.sh /opt/tritonserver/
COPY grpc_gcp_caip_pb2.py /opt/tritonserver/

ENTRYPOINT ["bash", "caip_entrypoint.sh"]
