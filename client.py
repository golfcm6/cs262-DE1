# Import socket module
import socket


class Session:
	def __init__(self, name, status):
		self.username = name
		self.status = status



session = Session("", "0")

def check_valid_username(u):
	if not u or len(u) > 10 or " " in u:
		print("enter text between 1-10 characters with no spaces")
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
			_, err = validity.split("|")
			print(err)
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
			_, err = validity.split("|")
			print(err)
			quickstart(s)
		
		else:
			# set to active session
			print("logged in as " + existing_username)
			session.status = "1"
			session.username = existing_username

	except:
		print("error in logging in, try again")
		# redirect to asking for new username again
		create_username(s)

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

def login_action(s):
	pass

def main():
	# local host IP '127.0.0.1'
	host = '10.250.248.85'

	# Define the port on which you want to connect
	port = 49153

	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

	# connect to server on local computer
	s.connect((host,port))

	quickstart(s)

	# EVERYTHING BELOW IS NOT DONE

	# keep asking for user to send messages until manually quit by a user trigger
	while True:

		# message you send to server
		message = input('\ntype your message lmao: ')

		# need user to input exit to break from connection
		if message == "exit":
			break
			
		# message sent to server
		s.send(message.encode('ascii'))

		# message received from server
		data = s.recv(1024)

		# print the received message
		# here it would be a reverse of sent message
		print('Received from the server :',str(data.decode('ascii')))

	# close the connection
	s.close()

if __name__ == '__main__':
	main()
