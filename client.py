# Import socket module
import socket


def main():
	# local host IP '127.0.0.1'
	host = '10.250.139.197'

	# Define the port on which you want to connect
	port = 49153

	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

	# connect to server on local computer
	s.connect((host,port))

	# require a username
	while True:
		username = input('Provide a username: ')
		# as long as username isn't empty, log them in
		if username:
			s.send(username.encode('ascii'))
			break



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
