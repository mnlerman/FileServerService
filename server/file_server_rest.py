import grpc
from flask import Flask, request, redirect
import os
import fileserver_pb2
import fileserver_pb2_grpc

app = Flask(__name__)


@app.route('/fileserver/', methods=['GET'])
@app.route('/fileserver/<path:path>', methods=['GET'])
def get_file(path: str = ''):
    base_dir = '..'
    request_path = path
    if len(path.strip()) == 0:
        return 'No file path to serve'

    with grpc.insecure_channel('localhost:5005') as channel:
        stub = fileserver_pb2_grpc.FileServerStub(channel)

        file_request = fileserver_pb2.RequestPath(path=os.path.join(base_dir, request_path))
        response_file = stub.GetFile(file_request)

        return response_file.contents



if __name__ == '__main__':
    app.run(debug=True, port=8082)
