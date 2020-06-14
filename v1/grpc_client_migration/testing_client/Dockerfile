FROM nvcr.io/nvidia/tritonserver:20.03-py3-clientsdk
 

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python get-pip.py

RUN pip install --upgrade google-api-python-client

RUN pip install jupyterlab

RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
RUN apt-get update
RUN apt-get install -y google-cloud-sdk

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.6  1

WORKDIR /workspace/src/clients/python/api_v1/examples

COPY grpc_gcp_caip_pb2.py .
COPY gcp_image_client4.py .

#CMD ["jupyter lab --ip 0.0.0.0 --no-browser --allow-root"]


#update-alternatives --config python
#update-alternatives  --set python /usr/bin/python3.6

#update-alternatives --install /usr/bin/python python /usr/bin/python3.6  1
