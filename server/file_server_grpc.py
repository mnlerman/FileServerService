from concurrent import futures
import grpc
import fileserver_pb2
import fileserver_pb2_grpc


class FileServerServicer(fileserver_pb2_grpc.FileServerServicer):

    def GetFile(self, request, context):
        response = fileserver_pb2.ResponseFile()
        with open(request.path, mode='r') as file:
            response.file_path = request.path
            response.contents = file.read()
            return response

    def StreamFile(self, request, context):
        with open(request.path, mode='r') as file:
            for line in file.readlines():
                response = fileserver_pb2.ResponseFile()
                response.file_path = request.path
                response.contents = line.strip()
                yield response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    fileserver_pb2_grpc.add_FileServerServicer_to_server(FileServerServicer(), server)
    server.add_insecure_port("localhost:5005")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
