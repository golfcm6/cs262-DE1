# import socket programming library
import socket

# import thread module
from _thread import *
import threading
import re

# called whenever a DS gets updated
ds_lock = threading.Lock()

# k, v = username, socket currently being used (0 if not logged in)
# reason for keeping k and just updating v to 0 if not logged in 
# (instead of deleting from dict) is so usernames dict can still be 
# used for easy account lookup
usernames = {}
# k, v = online socket, username - used for updating of username logged in status
# when client badly disconnects
online = {}
# k, v = username, {sender : list of messages they received from sender}
offline_messages = {}

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
			if c in online:
				ds_lock.acquire()
				usernames[online[c]] = 0
				del online[c]
				ds_lock.release()

			break

		client_input = client_input.decode("ascii")
		wire, message = client_input.split('|', 1)

		# first char in wire: 0 means not signed in, 1 means signed in
		# second char in wire: function being called

		server_response = ""

		# switch cases for the function being called

		fn = wire[1]
		match fn:

			# create username
			case '0':
				if message not in usernames:
					ds_lock.acquire()
					usernames[message] = c
					ds_lock.release()
					server_response = "t"
				else:
					server_response = "username taken"

			# login
			case '1':
				if message in usernames:
					if usernames[message] == 0:
						server_response = "t"
						ds_lock.acquire()
						usernames[message] = c
						# keep track of active username at a socket so we can log them out if they badly disconnect
						online[c] = message
						ds_lock.release()
					else:
						server_response = "already logged in"

				else:
					server_response = "username does not exist"

			# list accounts
			case '2':
				# no need to check if logged in, client end does this
				for u in usernames:
					# TODO: IF THIS NEVER ENDS, WE NEED TO TIME IT OUT
					# TODO: do we need to lock for the search? no right?
					try:
						if re.search(message, u):
							server_response += u + "|"
					except:
						server_response = 'regex error '
						break

				if len(server_response) != 0:
					server_response = server_response[:-1]
				else:
					server_response = 'f'

			# message
			case '3':
				# client end checks that u doesn't contain a |
				recipient, msg = message.split('|', 1)

				if recipient not in usernames:
					server_response = 'recipient does not exist'
					break

				# recipient online - send directly to them
				#TODO: no need to lock for the online send right?
				if usernames[recipient] != 0:
					# formatted_msg = '*** new message from ' + online[c] + ':' + msg + '***'
					formatted_msg = msg
					# send message to the socket recipient is currently logged in at
					try:
						usernames[recipient].send(formatted_msg.encode('ascii'))
						print('sent')
						server_response = 't'
					except:
						print('server error in sending message to online user')

				# recipient offline - must store
				else:
					ds_lock.acquire()
					if recipient in offline_messages:
						if online[c] in offline_messages[recipient]:
							offline_messages[recipient][online[c]].append(msg)
						else:
							offline_messages[recipient][online[c]] = [msg]
					else:
						offline_messages[recipient] = {}
						offline_messages[recipient][online[c]] = [msg]
					ds_lock.release()
					server_response = 't'
					
					# offline_messages[recipient][online[c]] 




			case other:
				print('invalid function call')

		print(server_response)
		server_response = server_response.encode('ascii')
		c.send(server_response)
		print('sent')

	c.close()
	if message in usernames:
		ds_lock.acquire()
		usernames[message] = 0
		ds_lock.release()
	if c in online:
		ds_lock.acquire()
		del online[c]
		ds_lock.release()

def main():

	# hunch here is that we have to make the host the IP of the server computer
	# otherwise you are just listening for everything
	# ash ip: 10.250.248.85
	host = '10.228.32.141'

	# reserve a port on your computer
	# in our case it is 12345 but it
	# can be anything
	port = 49153
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((host, port))
	print("socket binded to port", port)

	# put the socket into listening mode - we accept everything, so no need to specify a backlog
	s.listen()
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