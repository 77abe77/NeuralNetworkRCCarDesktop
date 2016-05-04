# nnrccar.py (Executable)
# Written By: Abe Millan


from multiprocessing import Process, Queue
import dirMap

BLE_DEVICE_NAME = "nn_rc_car" # HM-10 unit is programmed to this name

if __name__ == '__main__':
	nm = NetworkManager()
	if not nm.isOnline():
		print("Please connect to a network and try again")
		exit()

	print("========================NEURAL NETWORK RC CAR===========================")
	nm.startListening()
	print("Please connect mobile device to {}:{}".format(nm.getAddress(), nm.getPort()))
	print("Waiting...")
	nm.acceptClient()
	print("Successfully connected to {}".format(nm.getClientAddress))

	mainSocket = nm.connectionSocket()

	# Main Program Loop
	while(True):
		print("========================NEURAL NETWORK RC CAR===========================")
		print("1: Collect Training Data				2: List Training Data")
		print("3: Edit/Playback Training Data		4. Train a Data Set")
		print("5: Send Neural Network Parameters 	q. Quit")
		option = raw_input("Enter Option: ")

		# Collect Training Data
		if option == "1":
			# Set up Shared Memory between Video and Controller Processes
			recordingFlag = Value('B', 0)
			capturingFlag = Value('B', 1)

			# Set up the Bluetooth Connection for the Controller
			bm = BluetoothManager()
			btSocket = bm.deviceByName(BLE_DEVICE_NAME)
			if btSocket == -1 or btSocket == -2:
				print("Could not connect to nn_rc_car. Try again")
				break

			# Start the NetworkVideoPlayer as a new process
			p = Process(target = NetworkVideoClient.startUp,
			 			args = (mainSocket, recordingFlag, capturingFlag))
			p.start()

			# Start the RC Controller on the main process
			BluetoothRCCarController(recordingFlag=recordingFlag,
									 capturingFlag=capturingFlag,
									 bleDevice=btSocket)

			# Merge the Video Data with the Controller Data
			CreateVideoFile()
			CreateTrainingData()


		# List Training Data
		elif option == "2":
			listTrainingData()

		# Edit/Playback Training Data
		elif option == "3":
			filepath = listTrainingData()
			option = raw_input("Select a training data: ")
			if option > len(filepath) or option <= 0:
				print('Invalid Selection')
				break
			filepath = filepath[option-1] + 'directionVideo.txt'
			vp.playBack(filepath)

		# Train Neural Network
		elif option == "4":
			filepath = listTrainingData()
			option = raw_input("Select a training data: ")
			if option > len(filepath):
				print('Invalid Selection')
				break
			filepath = filepath[option] + 'directionVideo.txt'

			X, y = getTrainingData(filepath)
			nn = NeuralNetworkClassifieer(X, y)
			nn.train()
			nn.writeWeightsToFile('weights.txt')

		# Send Neural Network Parameters
		elif option == "5":
			filepath = listTrainingData()
			option = raw_input("Select a training data: ")
			if option > len(filepath):
				print('Invalid Selection')
				break
			filepath = filepath[option] + 'weights.txt'
			if not os.path.isfile(filepath):
				print("This Data Set has not been trained yet!")
				continue

		# Quit
		elif option == "q":
			break
		else:
			continue

	finally:
		mySocket.close()
		exit():
