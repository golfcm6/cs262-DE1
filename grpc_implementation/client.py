import grpc
import chat_server_pb2 as pb2
import chat_server_pb2_grpc as pb2_grpc
from concurrent import futures
import sys

session_username = ""

def check_valid_username(u):
	if not u or len(u) > 10 or " " in u or '|' in u:
		print("enter text between 1-10 characters with no spaces or |")
		return False
	return True

def create_username(stub):
    while True:
        new_username = input("Enter a new username: ")
        if check_valid_username(new_username):
            break
    print("creating username")
    new_user_req = pb2.User(username = new_username)

    # call create_user
    create_status = stub.create_user(new_user_req)
    print(create_status.status_result)

    # check if status was successful
    if create_status.status_result != "t":
        print("something went wrong")
        quickstart(stub)

def login(stub):
    while True:
        existing_username = input("Enter your username: ")
        if check_valid_username(existing_username):
            break
    print("logging in")
    login_req = pb2.User(username = existing_username)
    login_status = stub.login(login_req)

    print(login_status.status_result)

    # check if login worked correctly
    if login_status.status_result [0] != "t":
        print("something went wrong")
        quickstart(stub)

    # if worked correctly 
    else:
		# set to active session
        print("logged in as " + existing_username + '\n')
        offline_messages = login_status.status_result [1:]
        
        print("offline messages: \n")
    # TODO: figure out why empty dict is f lol
    if offline_messages == 'f':
        offline_messages = 'none'
        print(offline_messages)
    

def quickstart(stub):
	while True:
		login_choice = input("Enter c to create a new username or u to log in to existing account: ")
		# as long as username isn't empty, log them in
		if login_choice == "c":
			create_username(stub)
			break
		elif login_choice == "u":
			login(stub)
			break


def run():
    global session_username
    args = sys.argv[1:]
    assert len(sys.argv) == 2, f"provide host address"
    
    host = args[0]
    port = 49153


    with grpc.insecure_channel('{}:{}'.format(host, port)) as channel:
        stub = pb2_grpc.Chat_ServiceStub(channel)
        print("client connected")
        quickstart(stub)

if __name__ == "__main__":
    run()
        