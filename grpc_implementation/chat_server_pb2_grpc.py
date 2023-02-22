# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import chat_server_pb2 as chat__server__pb2


class Chat_ServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.send_message = channel.unary_unary(
                '/Chat_Service/send_message',
                request_serializer=chat__server__pb2.Text.SerializeToString,
                response_deserializer=chat__server__pb2.Status.FromString,
                )
        self.create_user = channel.unary_unary(
                '/Chat_Service/create_user',
                request_serializer=chat__server__pb2.User.SerializeToString,
                response_deserializer=chat__server__pb2.Status.FromString,
                )
        self.delete_user = channel.unary_unary(
                '/Chat_Service/delete_user',
                request_serializer=chat__server__pb2.User.SerializeToString,
                response_deserializer=chat__server__pb2.Status.FromString,
                )
        self.login = channel.unary_unary(
                '/Chat_Service/login',
                request_serializer=chat__server__pb2.User.SerializeToString,
                response_deserializer=chat__server__pb2.Status.FromString,
                )
        self.search_users = channel.unary_unary(
                '/Chat_Service/search_users',
                request_serializer=chat__server__pb2.Search.SerializeToString,
                response_deserializer=chat__server__pb2.Users.FromString,
                )
        self.detect_disconnect = channel.unary_unary(
                '/Chat_Service/detect_disconnect',
                request_serializer=chat__server__pb2.Status.SerializeToString,
                response_deserializer=chat__server__pb2.Void.FromString,
                )
        self.stream_chats = channel.unary_stream(
                '/Chat_Service/stream_chats',
                request_serializer=chat__server__pb2.Void.SerializeToString,
                response_deserializer=chat__server__pb2.Text.FromString,
                )


class Chat_ServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def send_message(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def create_user(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def delete_user(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def login(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def search_users(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def detect_disconnect(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def stream_chats(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_Chat_ServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'send_message': grpc.unary_unary_rpc_method_handler(
                    servicer.send_message,
                    request_deserializer=chat__server__pb2.Text.FromString,
                    response_serializer=chat__server__pb2.Status.SerializeToString,
            ),
            'create_user': grpc.unary_unary_rpc_method_handler(
                    servicer.create_user,
                    request_deserializer=chat__server__pb2.User.FromString,
                    response_serializer=chat__server__pb2.Status.SerializeToString,
            ),
            'delete_user': grpc.unary_unary_rpc_method_handler(
                    servicer.delete_user,
                    request_deserializer=chat__server__pb2.User.FromString,
                    response_serializer=chat__server__pb2.Status.SerializeToString,
            ),
            'login': grpc.unary_unary_rpc_method_handler(
                    servicer.login,
                    request_deserializer=chat__server__pb2.User.FromString,
                    response_serializer=chat__server__pb2.Status.SerializeToString,
            ),
            'search_users': grpc.unary_unary_rpc_method_handler(
                    servicer.search_users,
                    request_deserializer=chat__server__pb2.Search.FromString,
                    response_serializer=chat__server__pb2.Users.SerializeToString,
            ),
            'detect_disconnect': grpc.unary_unary_rpc_method_handler(
                    servicer.detect_disconnect,
                    request_deserializer=chat__server__pb2.Status.FromString,
                    response_serializer=chat__server__pb2.Void.SerializeToString,
            ),
            'stream_chats': grpc.unary_stream_rpc_method_handler(
                    servicer.stream_chats,
                    request_deserializer=chat__server__pb2.Void.FromString,
                    response_serializer=chat__server__pb2.Text.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Chat_Service', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Chat_Service(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def send_message(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Chat_Service/send_message',
            chat__server__pb2.Text.SerializeToString,
            chat__server__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def create_user(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Chat_Service/create_user',
            chat__server__pb2.User.SerializeToString,
            chat__server__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def delete_user(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Chat_Service/delete_user',
            chat__server__pb2.User.SerializeToString,
            chat__server__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def login(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Chat_Service/login',
            chat__server__pb2.User.SerializeToString,
            chat__server__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def search_users(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Chat_Service/search_users',
            chat__server__pb2.Search.SerializeToString,
            chat__server__pb2.Users.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def detect_disconnect(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Chat_Service/detect_disconnect',
            chat__server__pb2.Status.SerializeToString,
            chat__server__pb2.Void.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def stream_chats(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/Chat_Service/stream_chats',
            chat__server__pb2.Void.SerializeToString,
            chat__server__pb2.Text.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)