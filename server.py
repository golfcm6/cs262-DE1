# import socket programming library
import socket

# import thread module
from _thread import *
import threading

print_lock = threading.Lock()

counter = 0

# right now just making username tracker a list for ease, will eventually need to be
# a dictionary also tracking logged in status and address
users = {}


# thread function
def threaded(c, addr):
	print(addr)
	global counter

	getUsername = c.recv(1024)
	getUsername = getUsername.decode("ascii")
	if getUsername not in users:
		users[getUsername] = c
	
	while True:

		# data received from client
		data = c.recv(1024)
		if not data:
			print('Bye')

			# alter dictionary so IP set to 0
			users[getUsername] = 0
			break
		else:
			print_lock.acquire()
			wire = data.decode('ascii')

			# code for processing wire protocol should go here
			wire = wire.split("|")
			print(wire)
			recipient = wire[0]
			msg = wire[1]

			# after processing, direct arguments to the right function

			# msg = msg[::-1]
			# msg += ', ' + str(counter)

			# # reverse the given string from client
			data = msg.encode('ascii')
			sendSocket = users[recipient]
			# send back reversed string to client
			sendSocket.send(data)
			counter += 1
			print_lock.release()

	# connection closed
	c.close()


def main():
	# hunch here is that we have to make the host the IP of the server computer
	# otherwise you are just listening for everything
	host = "10.250.139.197"

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