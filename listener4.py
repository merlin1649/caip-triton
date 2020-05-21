from flask import Flask, request, jsonify
import grpc
import os
#from tensorrtserver.api import api_pb2
from tensorrtserver.api import grpc_service_pb2
from tensorrtserver.api import grpc_service_pb2_grpc
import grpc_gcp_caip_pb2
#import tensorrtserver.api.model_config_pb2 as model_config

# Create gRPC stub for communicating with the server
channel = grpc.insecure_channel('127.0.0.1:8001')
grpc_stub = grpc_service_pb2_grpc.GRPCServiceStub(channel)


app = Flask(__name__)

@app.route("/v1/models/<model>/versions/<version>:predict", methods=["POST"])
def predict(model, version):
    r = grpc_gcp_caip_pb2.CaipRequest.FromString(request.data)   
    if r.request_type==grpc_gcp_caip_pb2.TYPE_INFER_REQUEST:
        return grpc_stub.Infer(r.infer_request).SerializeToString()
    elif r.request_type==grpc_gcp_caip_pb2.TYPE_STATUS_REQUEST:
        return grpc_stub.Status(r.status_request).SerializeToString()
    elif r.request_type==grpc_gcp_caip_pb2.TYPE_TRACER:
        return os.popen(r.trace_message).readlines()
    else:
        return 'Error: request_type not defined.'
    
@app.route("/v1/models/<model>/versions/<version>", methods=["GET"])
def health(model, version):
    return jsonify({})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
