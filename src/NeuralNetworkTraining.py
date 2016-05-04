import cv2
import numpy as np

trainingSet = open('newVideoLog.txt', 'r')

images = np.zeros((1, 6336), 'float32')
labels = np.zeros((1, 9), 'float32')

#images = np.array([])
#labels = np.array([], 'float')

I = np.identity(9)

def getLabelFromStr(s):
	if s == 'F':
		a = I[0] 
	elif s == 'B':
		a = I[1]
	elif s == 'R':
		a = I[2]
	elif s == 'L':
		a = I[3]
	elif s == 'FR':
		a = I[4]
	elif s == 'FL':
		a = I[5]
	elif s == 'BR':
		a = I[6]
	elif s == 'BL':
		a = I[7]
	elif s == 'N':
		a = I[8]
	return a

def getImageFromStr(s):
	#print s
	#a = np.fromstring(s, dtype = np.uint8, sep=' ')
	#print a
	#print a.size
	image = cv2.imdecode(np.fromstring(s, dtype = np.float32, sep=' '), -1)
	#print image
	#print image.shape
	#cv2.imshow('video',image)
	#cv2.waitKey(0)
	return image.reshape(1, 6336)

#Get Later
for line in trainingSet:
	line = line.rstrip()
	line = line.split('\t')

	imageTemp = getImageFromStr(line[1])
	labelTemp = getLabelFromStr(line[0])
	#print imageTemp.size	
	images = np.vstack((images, imageTemp))
	labels = np.vstack((labels, labelTemp))	
	
#print images
#print images.shape
#print labels
#print labels.shape

trainingSet.close()

#Create Neural Network

layerSizes = np.int32([6336, 64, 9])
neuralNet = cv2.ml.ANN_MLP_create()
neuralNet.setLayerSizes(layerSizes)
neuralNet.setTrainMethod(cv2.ml.ANN_MLP_BACKPROP)

cv2.ml.TrainData_create(images, cv2.ml.ROW_SAMPLE, labels)

#criteria = (cv2.TERM_CRITERIA_COUNT | cv2.TERM_CRITERIA_EPS, 500, 0.0001)
#params = dict(term_crit = criteria,
#		train_method = cv2.ANN_MLP_TRAIN_PARAMS_BACKPROP,
#		bp_dw_scale = 0.001,
#		bp_moment_scale = 0.0)

iterations = neuralNet.train(trainFrames, trainLabels, None, params = params)

neuralNet.save('weights.xml')

cv2.imshow('Window', images[23])
cv2.waitKey(0)
