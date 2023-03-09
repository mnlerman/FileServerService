import grpc
from flask import Flask, request, redirect

import fileserver_pb2
import fileserver_pb2_grpc

app = Flask(__name__)


@app.route('/fileserver/', methods=['GET'])
@app.route('/fileserver/<path:path>', methods=['GET'])
def fileserver(path: str = ''):
    base_dir = '..'
    path = path
    if len(path.strip()) == 0:
        return 'No file path to serve'

    with grpc.insecure_channel('localhost:5005') as channel:
        stub = fileserver_pb2_grpc.FileServerStub(channel)

        file_request = fileserver_pb2.RequestPath(path=f'{base_dir}/{path}')
        response_file = stub.GetFile(file_request)

        return f'contents of {response_file.file_path}:\n{response_file.contents}'

    #return redirect(f'http://localhost:8081/thredds/fileServer/{path}')


if __name__ == '__main__':
    app.run(debug=True, port=50051)
