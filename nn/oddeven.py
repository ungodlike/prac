# -*- coding: utf-8 -*-
"""ANN2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1j1M5SeBk9J3MtTV4rn_BWy9MbGqCBgCS
"""

def initialize_network(n_inp, n_hid, n_out):
  network = list()
  hid_layer = [{'weights':[random() for i in range(n_inp+1)]} for i in range(n_hid)]
  network.append(hid_layer)
  out_layer = [{'weights':[random() for i in range(n_hid+1)]} for i in range(n_out)]
  network.append(out_layer)
  return network

#1 hidden layer; for 2, repeat beforementioned code

#seed(1)
#network = initialize_network(2, 1, 2) #2 inputs, 1 hidden, 2 outputs NEURONS (not layers)
#for layer in network:
#  print(layer)

#calculate neuron activation for an input
def activate(weights, inputs):
    activation = weights[-1] #this is the bias

    for i in range(len(weights)-1):
      activation += weights[i] * inputs[i] #inputs multiplied with corresponding weights

    return activation

#transfer neuron activation
def transfer(activation):
  return 1.0/(1.0 + exp(-activation)) #can use sigmoid too; 1.0/(1.0 + exp(-activation))

#forward propagate the input to a netork output
#this is repeated for every neuron in every layer

def forward_propagate(network, row):
  inputs = row #dataset row

  for layer in network:

    new_inputs = []

    for neuron in layer:
      activation = activate(neuron['weights'], inputs) #activation being done on every initial input, this activated value  
      neuron['output'] = transfer(activation)          #will be output for hidden and input for final output layer
      new_inputs.append(neuron['output'])              #storing the activated outputs of prev neurons as new inputs for next layer
    inputs = new_inputs                                #aka outputs from activated part
  return inputs

def transfer_derivative(output):                        #sumn to do with error
  return output *(1.0 - output)

def backward_propagate_error(network, expected):        #back propagate this error to change the weights later and so on 
	for i in reversed(range(len(network))):
		layer = network[i]
		errors = list()
		if i != len(network)-1:
			for j in range(len(layer)):
				error = 0.0
				for neuron in network[i + 1]:
					error += (neuron['weights'][j] * neuron['delta'])
				errors.append(error)
		else:
			for j in range(len(layer)):
				neuron = layer[j]
				errors.append(neuron['output'] - expected[j])
		for j in range(len(layer)):
			neuron = layer[j]
			neuron['delta'] = errors[j] * transfer_derivative(neuron['output'])

def update_weights(network, row, l_rate):             #updating new weights 
	for i in range(len(network)):
		inputs = row[:-1]
		if i != 0:
			inputs = [neuron['output'] for neuron in network[i - 1]]
		for neuron in network[i]:
			for j in range(len(inputs)):
				neuron['weights'][j] -= l_rate * neuron['delta'] * inputs[j]
			neuron['weights'][-1] -= l_rate * neuron['delta']

def train_network(network, train, l_rate, n_epoch, n_outputs):      #training this multilayer network post forward/backward propagate
	for epoch in range(n_epoch):
		sum_error = 0
		for row in train:
			outputs = forward_propagate(network, row)
			expected = [0 for i in range(n_outputs)]
			expected[row[-1]] = 1
			sum_error += sum([(expected[i]-outputs[i])**2 for i in range(len(expected))])
			backward_propagate_error(network, expected)
			update_weights(network, row, l_rate)
		print('>epoch=%d, lrate=%.3f, error=%.3f' % (epoch, l_rate, sum_error))

#odd even dataset with expected values
dataset = [[0,0,1,0],              #we'll use binary numbers here since numbers ending with 0 are even and 1 are odd,
 [0,1,0,1],                        #this will help capture, classify a feature whereas numbers themselves won't have a pattern
 [0,1,1,0],
 [1,0,0,1],[1,0,1,0],[1,1,0,1],[1,1,1,0]]
n_inputs = len(dataset[0]) - 1
n_outputs = len(set([row[-1] for row in dataset]))
network = initialize_network(n_inputs, 2, n_outputs)
train_network(network, dataset, 0.2, 5000, n_outputs)
for layer in network:
  print(layer)

def predict(network, row):
	outputs = forward_propagate(network, row)
	return outputs.index(max(outputs))

for row in dataset:                                 #printing values
	prediction = predict(network, row)
	print('Expected=%d, Got=%d' % (row[-1], prediction))