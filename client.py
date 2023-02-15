# Import socket module
import socket


def main():
	# local host IP '127.0.0.1'
	host = '127.0.0.1'

	# Define the port on which you want to connect
	port = 49153

	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

	# connect to server on local computer
	s.connect((host,port))

	# message you send to server
	message = input('\ntype your message lmao :')

	while True:

		# message sent to server
		s.send(message.encode('ascii'))

		# message received from server
		data = s.recv(1024)

		# print the received message
		# here it would be a reverse of sent message
		print('Received from the server :',str(data.decode('ascii')))

		break
	# close the connection
	s.close()

if __name__ == '__main__':
	main()
