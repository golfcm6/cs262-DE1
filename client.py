# Import socket module
import socket
import select
import sys

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

session = Session("", "0")

def check_valid_username(u):
	if not u or len(u) > 10 or " " in u or '|' in u:
		print("enter text between 1-10 characters with no spaces or |")
		return False
	return True

def create_username(s):
	while True:
		new_username = input("Enter a new username: ")
		if check_valid_username(new_username):
			break
	
	# wire 
	# 0 as first element to indicate not logged in, 0 as next element to indicate creating new username
	# | (pipe character)
	# username text 
	# make sure not active session
	assert(session.status == "0")
	data = session.status + "0|" + new_username

	# send wire to server
	s.send(data.encode("ascii"))
	validity = s.recv(1024)
	if not validity:
		print(SERVER_FAILURE)
		sys.exit()
	validity = validity.decode("ascii")

	if (validity != "t"):
		print(validity)
		quickstart(s)
	else:
		print("logged in as " + new_username)
		# set session to active and set username
		session.status = "1"
		session.username = new_username

# login to an existing username
def login(s):
	while True:
		existing_username = input("Enter your username: ")
		if check_valid_username(existing_username):
			break
	# wire 
	# 0 as first element to indicate not logged in, 1 as next element to indicate entering existing username
	# | (pipe character)
	# username text 
	# make sure not an active session
	assert(session.status == "0")
	data = session.status + "1|" + existing_username

	s.send(data.encode("ascii"))
	validity = s.recv(1024)
	if not validity:
		print(SERVER_FAILURE)
		sys.exit()
	validity = validity.decode("ascii")

	if (validity[0] != "t"):
		print(validity)
		quickstart(s)
	
	else:
		# set to active session
		print("logged in as " + existing_username + '\n')
		session.status = "1"
		session.username = existing_username

		offline_messages = validity[1:]

		print("offline messages: \n")
		#TODO: figure out why empty dict is f lol
		if offline_messages == 'f':
			offline_messages = 'none'
		print(offline_messages)

def quickstart(s):
	while True:
		login_choice = input("Enter c to create a new username or u to log in to existing account: ")
		# as long as username isn't empty, log them in
		if login_choice == "c":
			create_username(s)
			break
		elif login_choice == "u":
			login(s)
			break

# behavior is that the actual regex expression validity isn't checked - will return no results found if invalid
def account_search(s):
	regex_exp = input("Enter regex pattern to search through usernames: ")

	assert(session.status == '1')

	data = session.status + "2|" + regex_exp

	s.send(data.encode("ascii"))
	output = s.recv(1024)
	if not output:
		print(SERVER_FAILURE)
		sys.exit()
	output = output.decode('ascii')

	if output == 'f':
		print("no results found")
	else:
		print(output.split('|'))

def send_message(s):
	recipient = ''
	while True:
		recipient = input("Enter username to send message to: ")
		if check_valid_username(recipient):
			break

	msg = input("Enter message to send: ")

	data = session.status + "3|" + recipient + '|' + msg

	s.send(data.encode("ascii"))
	output = s.recv(1024)
	if not output:
		print(SERVER_FAILURE)
		sys.exit()
	output = output.decode('ascii')

	if output != 't':
		print(output)
	else:
		print('sent')

def delete_account(s):
	data = session.status + '4|' + session.username

	s.send(data.encode("ascii"))
	output = s.recv(1024)
	if not output:
		print(SERVER_FAILURE)
		sys.exit()
	output = output.decode('ascii')

	if output != 't':
		print(output)
	else:
		print('Account successfully deleted. Goodbye!')
		sys.exit()



def logged_in(s):
	assert(session.status == "1")

	while True:
		# once logged in, we constantly check if server has sent us something (incoming message)
		sockets_list = [sys.stdin, s]

		read_sockets, _, _ = select.select(sockets_list,[],[])

		for socks in read_sockets:
			if socks == s:
				message = s.recv(1024)
				if not message:
					print(SERVER_FAILURE)
					sys.exit()
				message = message.decode('ascii')
				print(message)

			else:
				print('\nWelcome, ' + session.username + '!')
				# try:
				message = input(client_home_msg)

				match message:
					case '2':
						account_search(s)
					case '3':
						send_message(s)
					case '4':
						delete_account(s)
					case 'exit':
						print('see ya')
						sys.exit()
				# except:
				# 	# EOF error from unit testing, sleep for the unit test
				# 	time.sleep(10)

def main():
	args = sys.argv[1:]
	assert len(sys.argv) == 2, f"provide server host address"

	# ash ip on harvard secure: 10.250.248.85
	# ash ip on eduroam: 10.228.32.141
	host = args[0]

	# Define the port on which you want to connect
	port = 49153

	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

	# connect to server on local computer
	s.connect((host,port))

	quickstart(s)

	# has all functionality for when logged in
	logged_in(s)
		
if __name__ == '__main__':
	main()
