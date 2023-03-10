import grpc
import chat_server_pb2 as pb2
import chat_server_pb2_grpc as pb2_grpc
from concurrent import futures

import threading
import re
import sys

class Chat_ServiceServicer(pb2_grpc.Chat_ServiceServicer):
    def __init__(self):
        # dictionary to track usernames
        # u, s = username, status (either 0, "logged in")
        self.usernames = {}

        # dictionary to hold offline_messages to deliver once users log in
        # k, v = receiving username, {sender : list of messages they received from sender}
        self.online_messages = {}

        # dictionary to hold offline_messages to deliver once users log in
        # k, v = receiving username, {sender : list of messages they received from sender}
        self.offline_messages = {}

        # threading lock
        self.ds_lock = threading.Lock()

    # function to compile, send, and delete offline messages given a user logging on
    def offline(self, queued_user):
        res = ""
        # if there are no offline messages for queued_user
        if queued_user not in self.offline_messages or self.offline_messages[queued_user] == {}:
            res = "f"
        else:
            # acquire the offline_messages for the queued_user
            res = self.offline_messages[queued_user]

            self.ds_lock.acquire()
	        # delete offline messages for the user who just logged in since we're delivering the message now
            self.offline_messages[queued_user] = {}
            self.ds_lock.release()
        return res

    # create a new user: User -> Status
    def create_user(self, request, context):
        print("Create Request Received: ")
        print(request)
        message = request.username
        # ensure the username hasn't been taken before
        if message not in self.usernames:
            # generate a new user and set as logged in
            self.ds_lock.acquire()
            self.usernames[message] = "logged in"
            self.ds_lock.release()

            server_response = "t"
        else:
            server_response = "username taken"
        
        return_status = pb2.Status(status_result = server_response)
        return return_status
    
    # login a user: User -> Status
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
                self.usernames[message] = "logged in"
                self.ds_lock.release() 

                # add to response any offline messages missed
                server_response += str(self.offline(message))
            else:
                server_response = "already logged in"
        else:
            server_response = "username doesn't exist"
        
        return_status = pb2.Status(status_result = server_response)
        return return_status
    
    # stream chats sent to user who's currently logged in: User -> stream Text_Returnable
    def stream_chats(self, request, context):
        # get the username
        user_req = request.username

        # continuously query until user logs out
        while self.usernames[user_req] == "logged in":
            # if there are new messages uploaded to the online_messages dictionary under user_req
            if user_req in self.online_messages and len(self.online_messages[user_req]) > 0:
                for key, value in list(self.online_messages[user_req].items()):
                    # format the message and yield it
                    formatted_msg = '*** new message from ' + key + '***\n' + str(value) + '\n***end message***'
                    msg = pb2.Text_Returnable(content = formatted_msg)
                    yield msg

                    # remove this message from the dictionary to avoid double send
                    del self.online_messages[user_req][key]
    
    # send a message: Text -> Status
    def send_message(self, request, context):
        # make sure the recipient exists
        if request.receiver not in self.usernames:
            server_response = pb2.Status(status_result = "recipient does not exist")
            return server_response

        # user is logged in, add to DS holding online messages
        if self.usernames[request.receiver] == "logged in":
            print("sending live message to logged in user")
            # if user already exists in the DS
            if request.receiver in self.online_messages:
                # if there are existing messages from same sender undelivered
                if request.sender in self.online_messages[request.receiver]:
                    self.online_messages[request.receiver][request.sender].append(request.content)
                else:
                    self.online_messages[request.receiver][request.sender] = [request.content]
            # otherwise, add the user to the DS and push the message into the queue
            else:
                self.online_messages[request.receiver] = {}
                self.online_messages[request.receiver][request.sender] = [request.content]
        
        # user not logged in
        else:
            print("sending offline message to user not logged in")
            # if user already exists in the DS
            if request.receiver in self.offline_messages:
                # if there are existing messages from same sender undelivered
                if request.sender in self.offline_messages[request.receiver]:
                    self.offline_messages[request.receiver][request.sender].append(request.content)
                else:
                    self.offline_messages[request.receiver][request.sender] = [request.content]
            # otherwise, add the user to the DS and push the message into the queue
            else:
                self.offline_messages[request.receiver] = {}
                self.offline_messages[request.receiver][request.sender] = [request.content]

        server_response = pb2.Status(status_result = "t")
        return server_response
    
    # logout a user: User -> Status
    def logout(self, request, context):
        assert(request.username in self.usernames)

        # set username to logged out
        self.ds_lock.acquire()
        self.usernames[request.username] = 0
        self.ds_lock.release()
        
        assert(self.usernames[request.username] == 0)


        server_response = pb2.Status(status_result = "t")
        return server_response
    
    # delete user: User -> Status
    def delete_user(self, request, context):
        try:
            # remove the username from the usernames dictionary and remove all unsent messages to this user
            del self.usernames[request.username]
            if request.username in self.offline_messages:
                del self.offline_messages[request.username]
            msg = "t"
        except Exception as _:
            msg = "error in deleting account"

        server_response = pb2.Status(status_result = msg)
        return server_response
    
    # search for users given a regex: Search -> Text_Returnable
    def search_users(self, request, context):
        server_response = ""
        # look through usernames and see if regex matches
        for u in self.usernames:
            try:
                if re.search(request.username_search, u):
                    server_response += u + "|"
            except Exception as _:
                server_response = "regex error"
                break
        
        # remove last pipe character if there are matches
        if len(server_response) != 0:
            server_response = server_response[:-1]
        else:
            server_response = "f"
        
        ret_response = pb2.Text_Returnable(content = server_response)
        return ret_response
        
            

def serve():
    args = sys.argv[1:]
    assert len(sys.argv) == 2, f"provide host address"
    
    host = args[0]
    port = 49153

    # start up the server and add the Chat_Service
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_Chat_ServiceServicer_to_server(Chat_ServiceServicer(), server)

    server.add_insecure_port('{}:{}'.format(host, port))
    print("server up and running")
    
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()