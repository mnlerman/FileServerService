from os import path

import grpc
import pytest

import fileserver_pb2
import fileserver_pb2_grpc

from server.file_server_utils import grpc_server_on
from test_data.test_constants import multiline_text


class TestGrpcEndpoints:
    channel = None
    stub = None

    def setup_class(self):
        self.channel = grpc.insecure_channel(f'localhost:5005')
        self.stub = fileserver_pb2_grpc.FileServerStub(self.channel)

    def teardown_class(self):
        self.channel.close()

    def test_is_connected(self):
        assert(grpc_server_on(self.channel))

    def test_get_file(self, tmp_path):
        test_path = path.join(tmp_path, 'get.txt')
        with open(test_path, 'w') as test_file:
            test_file.write(multiline_text)

        file_request = fileserver_pb2.RequestPath(path=test_path)
        response_file = self.stub.GetFile(file_request)

        assert response_file.contents == multiline_text

    def test_stream_file(self, tmp_path):
        test_path = path.join(tmp_path, 'stream.txt')
        with open(test_path, 'w') as test_file:
            test_file.write(multiline_text)

        request = fileserver_pb2.RequestPath(path=test_path)
        response_stream = self.stub.StreamFile(request)
        responses = list(response_stream)
        with open(test_path, 'r') as read_file:
            lines = read_file.readlines()

        assert len(responses) == len(lines)

        files_match = True
        for written_line, read_line in list(zip(responses, lines)):
            if not files_match:
                break
            files_match = written_line.contents == read_line.strip()

        assert files_match
