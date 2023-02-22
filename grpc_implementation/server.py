import grpc
import chat_server_pb2 as pb2
import chat_server_pb2_grpc as pb2_grpc
from concurrent import futures

import socket
from _thread import start_new_thread
import threading
import re
import sys

class Chat_ServiceServicer(pb2_grpc.Chat_ServiceServicer):
    def __init__(self):
        # dictionary to track usernames
        self.usernames = {}

        # self.online = {}

        # dictionary to hold offline_messages to deliver once users log in
        # k, v = receiving username, {sender : list of messages they received from sender}
        self.offline_messages = {}

        # threading lock
        self.ds_lock = threading.Lock()

    def offline(self, queued_user):
        res = ""
        if queued_user not in self.offline_messages or self.offline_messages[queued_user] == {}:
            res = "f"
        else:
            res = self.offline_messages[queued_user]
        
        self.ds_lock.acquire()
	    # delete offline messages for the user who just logged in since we're delivering the message now
        self.offline_messages[queued_user] = {}
        self.ds_lock.release()

        return res

    def create_user(self, request, context):
        print("Create Request Received: ")
        print(request)
        message = request.username
        if message not in self.usernames:
            self.ds_lock.acquire()
            self.usernames[message] = "logged in"
            self.ds_lock.release()
            server_response = "t"
        else:
            server_response = "username taken"
        
        return_status = pb2.Status(status_result = server_response)
        return return_status
    
    def login(self, request, context):
        print("Login Request Received: ")
        print(request)
        message = request.username

        # make sure this is an existing username
        if message in self.usernames:
            # make sure existing username isn't already logged in
            if self.usernames[message] == 0:
                server_response = "t"

                self.ds_lock.acquire()
                self.usernames[message] == "logged in"
                self.ds_lock.release() 

                # add to response any offline messages missed
                server_response += str(self.offline(message))
            else:
                server_response = "already logged in"
        else:
            server_response = "username doesn't exist"
        
        return_status = pb2.Status(status_result = server_response)
        return return_status




def serve():
    args = sys.argv[1:]
    assert len(sys.argv) == 2, f"provide host address"
    
    host = args[0]
    port = 49153

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    pb2_grpc.add_Chat_ServiceServicer_to_server(Chat_ServiceServicer(), server)
    server.add_insecure_port('{}:{}'.format(host, port))
    print("server up and running")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()