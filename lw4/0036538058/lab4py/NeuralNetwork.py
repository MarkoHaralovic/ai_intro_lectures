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

   def forward(self, input):
      self.input = input
      self.z = np.dot(input, self.weights) + self.bias
      self.output = self.activation(self.z) if self.activation is not None else  self.z
      return self.output,self.z
   
class NeuralNetwork():
   def __init__(self,neural_net_architecture:list):
      self.layers = []
      self.architecture = neural_net_architecture
      
      for layer in neural_net_architecture:
         self.layers.append(self._make_layer(input_size=layer["input_dim"],output_size=layer["output_dim"],activation=layer["activation"]))
               
   def _make_layer(self,input_size,output_size,activation):
      return FullyConnectedLayer(input_size,output_size,activation)
   
   def forward_pass(self, X):
        _X_activation = X
        _X_output = None
        for layer in self.layers:
            _X_activation, _X_output = layer.forward(_X_activation)
        return _X_activation,_X_output
   
def sigmoid(x):
    clipped_x = np.clip(x, -100, 100)
    return 1 / (1 + np.exp(-clipped_x))


def mean_squared_error(y, y_hat):
   y = np.asarray(y).flatten()
   y_hat = np.asarray(y_hat).flatten()
   return np.mean((y - y_hat) ** 2)/len(y)

