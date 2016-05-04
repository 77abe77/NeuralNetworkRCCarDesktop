# Author: Abe Millan
# Simple module to automatically listen to an open port on the network 
import random
import socket


class SocketFactory():
	def __init__(self):
		self.online = True
		try:
			# This method for getting the host name is required for Ubuntu
			# since gethostbyname returns local hostname
			dummySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			dummySocket.connect(('8.8.8.8', 80)) # Google's DNS address
		except socket.error, (value, _):
			self.online = False

		self.HOST_ADDRESS = dummySocket.getsockname()[0]
		dummySocket.close()

	def isOnline(self):
		return self.online

	# Starts to listen on a random non-registered port
	def startListening(self):
		portFlag = 1
		while(portFlag):
			randPort = random.randrange(49152, 65536) #Non-Registered Ports
			try:
				portFlag = 0
				self.tSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				self.tSock.bind((HOST_ADDRESS, randPort))
			# Try another port if there is a socket error
			except socket.error, (value, _):
				portFlag = 1		
		# All goes well case:
		self.tSock.listen(0)
	
	# Blocking Wrapper over .accept method
	def acceptClient():
		(self.connectionSocket, self.clientAddress) = serverSocket.accept()
	

		return connectionSocket
	def getAddress():
		return self.HOST_ADDRESS
	def getPort():
		return self.PORT
	def getClientAddress():
		return self.clientAddress
	def getConnectionSocket():
		return self.connectionSocket
		
