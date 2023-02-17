# import socket programming library
import socket

# import thread module
from _thread import *
import threading

# print_lock = threading.Lock()

# right now just making username tracker a list for ease, will eventually need to be
# a dictionary also tracking logged in status and address
usernames = {}
socket_to_curr_username = {}

# thread function - has all workflow logic
# client end does input error handling properly
def threaded(c, addr):
	while True:

		# data received from client
		# hangs here and takes in empty message
		client_input = c.recv(1024)
		if not client_input:
			print('client: ' + str(c) +  ' disconnected')
			# only happens when a user was logged in
			if c in socket_to_curr_username:
				usernames[socket_to_curr_username[c]] = 0
				del socket_to_curr_username[c]

			break
		client_input = client_input.decode("ascii")

		# print_lock.acquire()

		wire, message = client_input.split('|')

		# first char in wire: 0 means not signed in, 1 means signed in
		# second char in wire: function being called

		wire, message = client_input.split('|')

		server_response = "f"

		# switch cases for the function being called

		fn = wire[1]
		match fn:

			# create username
			case '0':
				# assert wire[0] == 0, f"already logged in: disconnect to create a new username"
				if message not in usernames:
					usernames[message] = c
					server_response = "t"
				else:
					server_response += " | username taken"

			# login
			case '1':
				# assert wire[0] == 0, f"already logged in: disconnect to login with a different username"
				if message in usernames:
					if usernames[message] == 0:
						server_response = "t"
						usernames[message] = c
						# keep track of active username at a socket so we can log them out if they badly disconnect
						socket_to_curr_username[c] = message
					else:
						server_response += " | already logged in"

				else:
					server_response += " | username does not exist"

			# case '2':

			# case '3':

			case other:
				print('invalid function call')

		print(server_response)
		server_response = server_response.encode('ascii')
		c.send(server_response)
		print('sent')

	c.close()
	usernames[message] = 0
	if c in socket_to_curr_username:
		del socket_to_curr_username[c]

def main():

	# hunch here is that we have to make the host the IP of the server computer
	# otherwise you are just listening for everything
	# ash ip: 10.250.248.85
	host = '10.250.248.85'

	# reserve a port on your computer
	# in our case it is 12345 but it
	# can be anything
	port = 49153
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((host, port))
	print("socket binded to port", port)

	# put the socket into listening mode
	s.listen(5)
	print("socket is listening")

	# a forever loop until client wants to exit
	while True:
		# establish connection with client
		c, addr = s.accept()

		print('Connected to :', addr[0], ':', addr[1])

		# Start a new thread and return its identifier
		start_new_thread(threaded, (c, addr))
	s.close()


if __name__ == '__main__':
	main()