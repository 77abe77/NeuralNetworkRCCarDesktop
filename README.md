<h1>Neural Network RC Car (Desktop Code)</h1>


**This program works together with the** [NeuralNetworkRCCar iPhone application](https://github.com/77abe77/NeuralNetworkRCCar)

<h2>External Dependencies</h2>
+ OpenCV 2+
+ numpy
+ pygame

<h2>USAGE</h2>
<p> Make the python file executable </p>

```
chmod +x nnrccar.py
```

<p> Run the program </p>
```
./nnrccar
```


<h4>Option 1: Collecting Training Data</h4>

<p>Selecting option one will set up two concurrent processes. One listening to
keyboard input and one waiting for video frames.</p>

1. Place the iPhone on the RC Car.
2. Press a directional key to start streaming and recording.
3. Start driving the car around your assembled path.
4. To quit the program press Q (Upon quiting the program will save a txt file of direction keys mapped to raw grayscale pixel data AKA this is your training set)


  <h5>Time to Train the Neural Network</h5>


  1. Open MATLAB or OCTAVE
  2. Navigate to NeuralNetworkServer/src/
  3. Run getTrainingData.m (This script loads direction input into an X vector and pixel data into y vector and saves it into a .mat file)
  4. Navigate to NeuralNetworkServer/src/NeuralNetwork/
  5. Run ex4.m (This code is a modification of project 4 of the online Stanford Machine Class. It runs a backpropogation algorithm to train a 3 layer neural network.)
  6. Navigate back to NeuralNetworkServer/src/
  7. Run prepareData.m (This will load the trained weights to a txt file for them to be sent to the iPhone)
