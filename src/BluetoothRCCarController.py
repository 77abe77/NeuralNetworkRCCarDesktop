# RCController.py
# Written By: Abe Millan

import sys
import time
import pygame
from pygame.locals import *


directionMap = {'FR': 5, 'FL': 6, 'BR': 7, 'BL': 8, 'F': 1, 'B': 2, 'R': 3, 'L': 4, 'N': 0}
def startUp(bleDevice, recordingFlag, capturingFlag):
    BluetoothRCCarController(bleDevice, recordingFlag, capturingFlag)

class BluetoothRCCarController():
	""" RCController class operates in two modes:
	1) Normal: Responsible for listening to and recording keyboard inputs.
	If there is a queue passed in it will be used to communicate with
	the VideoClient object. If there is a serial path passed in
	it will be used to communicate keyboard directions to it.
	2) Autonomous: Responsible for recieving controls from socket and
	sending it to the serial device specified in the variable serialPath
	In this mode the autonomous argument should be set to True and
	a socket object should be passed in"""
	def __init__(self, recordingFlag, stopCapturingFlag, bleDevice):
		# Instance variables:
		# self.on - Flag when user presses q the controller stops
		# self.serialConnection - used for communication with Arduino
		# self.bleDevice - used for communication with bluetooth device
		# self.communicationQ - (NORMAL) used for IPC with VideoClient object
		# self.controlLog - (NORMAL) file used to record controls with time intervals
		# self.oldTime - (NORMAL) time a key was pushed in
		# self.stack - (NORMAL) used to store history of only direction key presses
		# self.count - (NORMAL) used to differentiate the first key press

		self.on = True
        self.recordingFlag = recordingFlag
        self.stopCapturingFlag = stopCapturingFlag

		self.controlLog = open("../supportingFiles/controlLog.txt", "wb")


        pygame.init()
		print("Press Any Direction To Start Moving")
        print("Press R to toggle recording")
		print("Press Q to quit")


		self.record()

	def _getDirection(self, key_input):
        """This internal function defines the label mapping for the
            RC Controls """
		temp = None
		if key_input[pygame.K_UP] and key_input[pygame.K_RIGHT]:
			temp = "FR"
		elif key_input[pygame.K_UP] and key_input[pygame.K_LEFT]:
			temp = "FL"
		elif key_input[pygame.K_DOWN] and key_input[pygame.K_RIGHT]:
			temp = "BR"
		elif key_input[pygame.K_DOWN] and key_input[pygame.K_LEFT]:
			temp = "BL"
        # simple orders
		elif key_input[pygame.K_UP]:
			temp = "F"
		elif key_input[pygame.K_DOWN]:
			temp = "B"
		elif key_input[pygame.K_RIGHT]:
			temp = "R"
		elif key_input[pygame.K_LEFT]:
			temp = "L"

		return temp

	def record(self):
        self.oldTime = 0
        self.stack = []
		try:
			while self.on:
				for event in pygame.event.get():

					curTime = int(time.time() * 1000)

					if event.type == KEYDOWN:
						# Alerts VideoClient object to start

						key_input = pygame.key.get_pressed()

						direction = self._getDirection(key_input)
						if direction != None:
							self.stack.append(direction)

						# Quiting key
						elif key_input[pygame.K_x] or key_input[pygame.K_q]:
							print('Exit')
							self.on = False
                            self.bleDevice.send("0")
							continue

						# Calibrate key
						elif key_input[pygame.K_c]:
							print('Calibrate')
							self.bleDevice.send("c")
							continue
                        # Recording key
						elif key_input[pygame.K_r]:
                            print('Recording')
                            if self.recordingFlag.value:
                                self.recordingFlag.value = 0
                            else:
                                self.recordingFlag.value = 1
						# Gets the current direction, prints it and writes it to
						# Arduino
						if (len(self.stack) - 1) >= 0:
							print(self.stack[len(self.stack)-1])
							strToWrite = str(directionMap[self.stack[len(self.stack) - 1]])
							self.bleDevice.send(strToWrite)

						# For the purposes of logging controls:
						# If there is only one thing in stack, no direction buttons were
						# pressed before
						if len(self.stack) == 1:
							st = 'N'
						elif len(self.stack) > 1:
							st = self.stack[0]

					elif event.type == pygame.KEYUP:
						key_input = pygame.key.get_pressed()
						direction = self._getDirection(key_input)

						# Makes sure key up is a directional key
						if len(self.stack) != 0:
							st = self.stack.pop()

						# If there is nothing in the directional key stack,
						# the current instruction is nothing. Send 0 to Arduino
						if len(self.stack) == 0:
							elif s
								self.bleDevice.send(str(0))
							print('N')
						else:
							if direction != self.stack[0]:
								self.stack[0] = direction
							self.bleDevice.send(str(directionMap[self.stack[0]]))
							print(self.stack[0])

					if self.count != 0:
						self.controlLog.write("{}\t{}\t{}\n".format(self.oldTime, curTime, st))

					self.oldTime = curTime
					self.count = 1
		finally:
			self.capturingFlag.value = 0
			self.controlLog.close()


#Simple Test of Bluetooth
if __name__ == '__main__':
	BluetoothRCCarController()
