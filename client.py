# Import socket module
import socket
import select
import sys


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

# new username
def create_username(s):
	while True:
		new_username = input("Enter a new username: ")
		if check_valid_username(new_username):
			break
	
	# wire 
	# 0 as first element to indicate not logged in, 0 as next element to indicate creating new username
	# | (pipe character)
	# username text 
	try:
		# make sure not active session
		assert(session.status == "0")
		data = session.status + "0|" + new_username

		# send wire to server
		s.send(data.encode("ascii"))
		validity = s.recv(1024)
		validity = validity.decode("ascii")

		if (validity != "t"):
			print(validity)
			quickstart(s)
		else:
			print("logged in as " + new_username)

			# set session to active and set username
			session.status = "1"
			session.username = new_username
		
	except Exception as e:
		print(repr(e))
		print("error in creating username, try again")
		# redirect to asking for new username again
		create_username(s)



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
	try:
		# make sure not an active session
		assert(session.status == "0")

		data = session.status + "1|" + existing_username

		s.send(data.encode("ascii"))

		validity = s.recv(1024)
		validity = validity.decode("ascii")

		if (validity != "t"):
			print(validity)
			quickstart(s)
		
		else:
			# set to active session
			print("logged in as " + existing_username)
			session.status = "1"
			session.username = existing_username

	except:
		print("error in logging in, try again")
		# redirect to logging in again
		login(s)

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
	output = output.decode('ascii')

	if output != 't':
		print(output)
	else:
		print('sent')



def logged_in(s):
	# keep asking for user to send messages until manually quit by a user trigger
	assert(session.status == "1")

	while True:
		# once logged in, we constantly check if server has sent us something (incoming message)
		sockets_list = [sys.stdin, s]

		read_sockets, write_socket, error_socket = select.select(sockets_list,[],[])

		for socks in read_sockets:
			if socks == s:
				message = s.recv(1024)
				message = message.decode('ascii')
				print(message)
			else:
				# message you send to server
				message = input('\nWelcome, ' + session.username + '! Enter:\n2    -->  regex search for accounts\n3    --> send message\nexit --> logout\n')

				match message:
					case '2':
						account_search(s)
					case '3':
						send_message(s)
					case 'exit':
						print('see ya')
						break

def main():
	# local host IP '127.0.0.1'
	host = '10.228.32.141'

	# Define the port on which you want to connect
	port = 49153

	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

	# connect to server on local computer
	s.connect((host,port))

	quickstart(s)

	# has all functionality for when logged in
	logged_in(s)
		
	# close the connection
	s.close()

if __name__ == '__main__':
	main()
