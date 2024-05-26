import numpy as np 

"""
   NOTE: neural_net_architecture should be a list looking like this  :
   [{"input_dim": 2, "output_dim": 4, "activation": "relu"},
    {"input_dim": 4, "output_dim": 6, "activation": "relu"}]
    Inspiration : https://towardsdatascience.com/lets-code-a-neural-network-in-plain-numpy-ae7e74410795
"""
class Layer():
   def __init__(self,input_size,output_size,activation):
      self.weights = np.random.rand(input_size,output_size)
      self.bias = np.random.rand(1,output_size)
      self.activation = activation
      return self
   def forward(self,input):
      self.output = np.dot(input,self.weights) + self.bias
      return self.output
   
class NeuralNetwork():
   def __init__(self,neural_net_architecture:list):
      self.input_size = None
      self.output_size = None
      self.layers = list()
      
      for layer_id,layer in  enumerate(neural_net_architecture):
         if layer_id == 0:
            self.input_size = layer["input_dim"]
         self.layers[layer_id] = self._make_layer(input_size=layer["input_dim"],output_size=layer["output_dim"],activation=layer["activation"])
            
   def sigmoid(self,input):
      pass
   
   def _make_layer(self,input_size,output_size,activation):
      return Layer(input_size,output_size,activation)
   
   def forward_pass(self):
      pass
   
