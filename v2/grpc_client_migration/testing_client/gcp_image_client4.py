from tensorrtserver.api import grpc_service_pb2
from functools import partial
import grpc_gcp_caip_pb2
import grpc_image_client
import requests
import argparse

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action="store_true", required=False, default=False)
    #parser.add_argument('-a', '--async', dest="async_set", action="store_true", required=False)
    #parser.add_argument('--streaming', action="store_true", required=False, default=False)
    parser.add_argument('-m', '--model-name', type=str, required=True)
    parser.add_argument('-x', '--model-version', type=int, required=False)
    parser.add_argument('-b', '--batch-size', type=int, required=False, default=1)
    parser.add_argument('-c', '--classes', type=int, required=False, default=1)
    parser.add_argument('-s', '--scaling', type=str, choices=['NONE', 'INCEPTION', 'VGG'],required=False, default='NONE')
    parser.add_argument('-u', '--url', type=str, required=False, default='localhost:8001')
    parser.add_argument('image_filename', type=str, nargs='?', default=None)
    
    FLAGS = parser.parse_args()
    
    predict_url = "http://{}/predict".format(FLAGS.url)
    headers = {
      'Content-Type': 'text/plain'
    }

    # Prepare request for Status gRPC
    status_request = grpc_service_pb2.StatusRequest(model_name=FLAGS.model_name)
    caip_request = grpc_gcp_caip_pb2.CaipRequest(request_type=grpc_gcp_caip_pb2.TYPE_STATUS_REQUEST, status_request = status_request)

    # CaipRequest message type send, StatusResponse message type receive
    status_response = grpc_service_pb2.StatusResponse().FromString(requests.request("POST", predict_url, headers=headers, data = caip_request.SerializeToString()).content)    

    # Make sure the model matches our requirements, and get some
    # properties of the model that we need for preprocessing
    input_name, output_name, c, h, w, format, dtype = grpc_image_client.parse_model(status_response, FLAGS.model_name, FLAGS.batch_size, FLAGS.verbose)

    filledRequestGenerator = partial(grpc_image_client.requestGenerator, input_name, output_name, c, h, w, format, dtype, FLAGS)

    # Send requests of FLAGS.batch_size images. If the number of
    # images isn't an exact multiple of FLAGS.batch_size then just
    # start over with the first images until the batch is filled.
    result_filenames = []
    infer_requests = []
    infer_responses = []

    # CaipRequest message type send, InferResponse message type receive
    for infer_request in filledRequestGenerator(result_filenames):
        caip_request = grpc_gcp_caip_pb2.CaipRequest(request_type=grpc_gcp_caip_pb2.TYPE_INFER_REQUEST, infer_request = infer_request)
        infer_responses.append(grpc_service_pb2.InferResponse().FromString(requests.request("POST", predict_url, headers=headers, data = caip_request.SerializeToString()).content))

    idx = 0
    for infer_response in infer_responses:
        print("Request {}, batch size {}".format(idx, FLAGS.batch_size))
        grpc_image_client.postprocess(infer_response.meta_data.output, result_filenames[idx], FLAGS.batch_size)
        idx += 1

