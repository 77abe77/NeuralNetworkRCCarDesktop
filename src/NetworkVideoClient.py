# NetworkVideoPlayer.py
# Written By: Abe Millan

import threading
import numpy as np
import cv2

# This function's sole purpose is for launching the NetworkVideoPlayer class
# as a seperate process
def startUp(mainSocket, recordingFlag, capturingFlag):
	NetworkVideoPlayer(mainSocket, recordingFlag, capturingFlag)

class NetworkVideoPlayer():
	""" VideoClient class operates by accepting a socket in as input and
	recieves JPEG compressed video frames from a remote device. The
	frames are then recorded onto a file in a seperate thread"""
	def __init__(self, socketConnection=None, recordingFlag, capturingFlag):
		# videoLog File Instance Variable
		self.videoLog = open("../supportingFiles/video.txt", "w")

		if socketConnection == None:
			import NetworkManager
			nm = NetworkManager()
			nm.startListening()
			print("Please connect mobile device to {}:{}".format(nm.getAddress(), nm.getPort()))
			print("Waiting...")
			nm.acceptClient()
			print("Successfully connected to {}".format(nm.getClientAddress))
		else:
			self.connectionSocket = socketConnection

		self.recordingFlag = recordingFlag
		self.capturingFlag = capturingFlag

		# Complete Video Frame Instance Variable
		self.frameArray = np.array([], dtype = 'B')

		# Start up OpenCV Video Window
		cv2.namedWindow('Video Stream')

	def _containsEOF(self, frame):
		retVal = False
		possibleEOF = np.where(frame == 215)[0]
		if possibleEOF.size != 0:
			indexEOF = -1
			for i in range(possibleEOF.size):
				#If the previous byte is 255, then you have the /255/215 EOF marker
				if self.frameArray[possibleEOF[i] - 1] == 255:
					indexEOF = possibleEOF[i]
					break
			if indexEOF != -1:
				retVal = True
		return retVal
	def startCapturing(self):
		try:
			while(self.keepCapturing):
				# pixelArray is a buffer for the fragmented network data
				# self.frameArray will append pixelArrays until a full frame has been stored
				pixelArray = np.fromstring(self.connectionSocket.recv(4096), dtype = np.uint8)
				self.frameArray = np.append(self.frameArray, pixelArray)

				if _containsEOF(self.frameArray):
					remainingFrame = self.frameArray[indexEOF + 1:]
					deleteIndex = np.arange((indexEOF - 9), self.frameArray.size)

					#Get the timestamp data before deleting it from self.frameArray
					timestampArray = self.frameArray[(indexEOF - 9):(indexEOF - 1)]

					self.frameArray = np.delete(self.frameArray, deleteIndex)

					timestamp = timestampArray.view(np.uint64)[0]

					#Write To File - Try one of Two options
					#a) Use Python threading


					image = cv2.imdecode(self.frameArray, -1)

					if self.recording:
						thr = threading.Thread(target = self.writeFrames, args = (timestamp, image))
						thr.start()
						cv.putText(image, "Recording" )

							# Forces frames to be 352x288
					image = cv2.resize(image, (352, 288))
					cv2.imshow('Video Stream', image)
					cv2.waitKey(1)

					self.frameArray = remainingFrame
			finally:
				# Give signal to source to stop sen
				self.connectionSocket.send("Q")
				#Clean Up
				cv2.destroyWindow('Video Stream')
				self.emptySocket(self.connectionSocket)
				self.videoLog.close()
				print("Finished Recording")

	def writeFrames(self, timestamp, frameArray):
		self.videoLog.write("{}\t".format(timestamp))
		frameArray.tofile(self.videoLog, " ")
		self.videoLog.write("\n")

	def emptySocket(self, sock):
		"""Clears the video buffer by stopping at the postamble 0 255"""
		while sock.recv(1) != chr(0):
			if sock.recv(1) != chr(255):
				break



if __name__ == '__main__':
	vm = videoClient()
