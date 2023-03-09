import grpc
import fileserver_pb2_grpc
import fileserver_pb2

import time


def run():
    with grpc.insecure_channel('localhost:5005') as channel:
        stub = fileserver_pb2_grpc.FileServerStub(channel)

        file_path = input('Which file would you like to serve?\n')
        is_stream = input('Would you like to get the entire file or stream the file?\n'
                       'press 0 to get entire file\n'
                       'press 1 to stream the file\n')


        if int(is_stream):
            file_request = fileserver_pb2.RequestPath(path=file_path)
            response_file = stub.StreamFile(file_request)

            print(f'streaming contents of {file_path}:')

            for line in response_file:
                print(line.contents)
                time.sleep(1)
        else:
            file_request = fileserver_pb2.RequestPath(path=file_path)
            response_file = stub.GetFile(file_request)

            print(f'contents of {response_file.file_path}:\n{response_file.contents}')


if __name__ == '__main__':
    run()

