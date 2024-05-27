import numpy as np 

"""
   NOTE: neural_net_architecture should be a list looking like this  :
   [{"input_dim": 2, "output_dim": 4, "activation": "relu"},
    {"input_dim": 4, "output_dim": 6, "activation": "relu"}]
    Inspiration : https://towardsdatascience.com/lets-code-a-neural-network-in-plain-numpy-ae7e74410795
"""

class FullyConnectedLayer():
   def __init__(self,input_size,output_size,activation):
      self.weights = np.random.uniform(low=-0.01, high=0.01, size=(input_size, output_size))
      self.bias = np.random.uniform(low=-0.01, high=0.01, size=(1, output_size))

      self.activation = activation

   def forward(self,input):
      self.input = input
      self.z = np.dot(input,self.weights) + self.bias
      self.output = self.activation(self.z) if self.activation is not None else self.z
      return self.output,self.z
   
class NeuralNetwork():
   def __init__(self,neural_net_architecture:list):
      self.input_size = None
      self.output_size = None
      self.layers = []
      self.architecture = neural_net_architecture
      
      for layer_id,layer in  enumerate(neural_net_architecture):
         if layer_id == 0:
            self.input_size = layer["input_dim"]
         if layer_id == len(neural_net_architecture)-1:
            self.output_size = layer["output_dim"]
         self.layers.append(self._make_layer(input_size=layer["input_dim"],output_size=layer["output_dim"],activation=layer["activation"]))
               
   def _make_layer(self,input_size,output_size,activation):
      return FullyConnectedLayer(input_size,output_size,activation)
   
   def forward_pass(self, X):
        _X_activation = X
        _X_output = None
        for layer in self.layers:
            _X_activation, _X_output = layer.forward(_X_activation)
        return _X_activation,_X_output
   
def sigmoid(input):
      return 1/(1+np.exp(-input))

def mean_squared_error(y,y_hat):
   sum = 0.0
   _len = len(y)
   for i in range(_len):
      sum += (y[i]-y_hat[i])**2
   return sum/_len

