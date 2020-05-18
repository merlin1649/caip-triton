from flask import Flask, request
import grpc
#from tensorrtserver.api import api_pb2
from tensorrtserver.api import grpc_service_pb2
from tensorrtserver.api import grpc_service_pb2_grpc
import grpc_gcp_caip_pb2
#import tensorrtserver.api.model_config_pb2 as model_config

# Create gRPC stub for communicating with the server
channel = grpc.insecure_channel('127.0.0.1:8001')
grpc_stub = grpc_service_pb2_grpc.GRPCServiceStub(channel)


app = Flask(__name__)

@app.route('/predict', methods=["POST"])
def predict():
    r = grpc_gcp_caip_pb2.CaipRequest.FromString(request.data)   
    if r.request_type==grpc_gcp_caip_pb2.TYPE_INFER_REQUEST:
        return grpc_stub.Infer(r.infer_request).SerializeToString()
    elif r.request_type==grpc_gcp_caip_pb2.TYPE_STATUS_REQUEST:
        return grpc_stub.Status(r.status_request).SerializeToString()
    else:
        return 'Error: request_type not defined.'

if __name__ == '__main__':
    app.run()
