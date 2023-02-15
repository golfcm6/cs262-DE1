# import socket programming library
import socket

# import thread module
from _thread import *
import threading

print_lock = threading.Lock()

counter = 0


# thread function
def threaded(c):
	global counter
	while True:

		# data received from client
		data = c.recv(1024)
		if not data:
			print('Bye')
			# lock released on exit
			print_lock.release()
			break

		msg = data.decode('ascii')
		msg = msg[::-1]
		msg += ', ' + str(counter)

		# reverse the given string from client
		data = msg.encode('ascii')

		# send back reversed string to client
		c.send(data)
		counter += 1

	# connection closed
	c.close()


def main():
	host = ""

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

		# lock acquired by client
		print_lock.acquire()
		print('Connected to :', addr[0], ':', addr[1])

		# Start a new thread and return its identifier
		start_new_thread(threaded, (c,))
	s.close()


if __name__ == '__main__':
	main()