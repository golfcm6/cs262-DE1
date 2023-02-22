import grpc
import chat_server_pb2 as pb2
import chat_server_pb2_grpc as pb2_grpc
import sys
import threading


SERVER_FAILURE = "server offline, chat app dead :("
client_home_msg = """
Enter:
2    --> regex search for accounts
3    --> send message
4    --> delete account
exit --> logout\n
"""

class Session:
	def __init__(self, name, status):
		self.username = name
		self.status = status

# start up a new session
session = Session("", "0")

# helper function to check if a username is formed well
def check_valid_username(u):
	if not u or len(u) > 10 or " " in u or '|' in u:
		print("enter text between 1-10 characters with no spaces or |")
		return False
	return True

# User -> Status
def create_username(stub):
    global session
    # get a username from the user
    while True:
        new_username = input("Enter a new username: ")
        if check_valid_username(new_username):
            break

    print("creating username")
    new_user_req = pb2.User(username = new_username)

    # call create_user with the input
    create_status = stub.create_user(new_user_req)
    print(create_status.status_result)

    # check if status was successful
    if create_status.status_result != "t":
        print("something went wrong")
        quickstart(stub)
    else:
        # set status to active
        session.status = "1"
        session.username = new_username

# User -> Status
def login(stub):
    global session
    # get a username
    while True:
        existing_username = input("Enter your username: ")
        if check_valid_username(existing_username):
            break
    print("logging in")
    login_req = pb2.User(username = existing_username)

    login_status = stub.login(login_req)

    # check if login worked correctly

    # didn't work correctly, reroute to start
    if login_status.status_result [0] != "t":
        print("something went wrong")
        quickstart(stub)

    # worked correctly 
    else:
        print("logged in as " + existing_username + '\n')

        # print out offline messages
        offline_messages = login_status.status_result [1:]
        print("offline messages: \n")
        if offline_messages == 'f':
            offline_messages = 'none'
        
        print(offline_messages)
        
        # set to active user
        session.username = existing_username
        session.status = "1"
        
# flow for onboarding user
def quickstart(stub):
	while True:
		login_choice = input("Enter c to create a new username or u to log in to existing account: ")

		if login_choice == "c":
			create_username(stub)
			break

		elif login_choice == "u":
			login(stub)
			break

# Text -> Status
def send_message(stub):
    recipient = ""
    while True:
        recipient = input("Enter username to send message to: ")
        if check_valid_username(recipient):
            break

    msg = input("Enter message to send: ")

    # message from current user to recipient with msg as content
    complete_message = pb2.Text(sender = session.username, receiver = recipient, content = msg)
    server_response = stub.send_message(complete_message)

    if server_response.status_result != 't':
        print(server_response.status_result)
    else:
        print('sent')

# User -> Status
def logout(stub, forever):
    global session

    logout_user = pb2.User(username = session.username)
    server_response = stub.logout(logout_user)
    assert(server_response.status_result == "t")

    # forever is true if deleting user permanently
    if forever:
        print("deleting user: " + session.username)

        del_user = pb2.User(username = session.username)
        server_response = stub.delete_user(del_user)

        if server_response.status_result != "t":
            print(server_response.status_result)
        else:
            print('Account successfully deleted. Goodbye!')

    # log out of active session
    session.username = ""
    session.status = "0"

# receive a stream from stream_chats and print them out as they come
def listen_to_stream(stub):
    cur_user = pb2.User(username = session.username)
    stream = stub.stream_chats(cur_user)
    for el in stream:
        print(el.content)
    return

# Search -> Text_Returnable
def account_search(stub):
    regex_exp = input("Enter regex pattern to search through usernames: ")
    new_search = pb2.Search(username_search = regex_exp)
    server_response = stub.search_users(new_search)

    if server_response.content[0] != "f":
        print(server_response.content.split('|'))
    else:
        print("no results found")

# once user logged in
def logged_in(stub):
    global session
    assert(session.status != "0")
    assert(session.username)

    # start a thread to listen for new messages
    threading.Thread(target=listen_to_stream, args=(stub,)).start()

    # flow for letting user trigger behavior
    while True:
        print('\nWelcome, ' + session.username + '!')
        message = input(client_home_msg)
        match message:
            case '2':
                account_search(stub)
            case '3':
                send_message(stub)
            case '4':
                logout(stub, True)
                sys.exit()
            case 'exit':
                logout(stub, False)
                print('see ya')
                sys.exit()


def run():
    global session
    args = sys.argv[1:]
    assert len(sys.argv) == 2, f"provide host address"
    
    host = args[0]
    port = 49153

    # connect to grpc channel and generate stub
    with grpc.insecure_channel('{}:{}'.format(host, port)) as channel:
        stub = pb2_grpc.Chat_ServiceStub(channel)
        print("client connected")

        quickstart(stub)
        logged_in(stub)

if __name__ == "__main__":
    run()
        