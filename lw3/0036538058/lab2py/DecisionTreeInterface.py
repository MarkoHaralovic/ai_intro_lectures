from abc import ABC, abstractmethod

class DecisionTree(ABC):
   @abstractmethod
   def __init__(self,*args, **kwargs):
      return NotImplementedError()
   @abstractmethod
   def fit(self,X,y):
      raise NotImplementedError()
   @abstractmethod
   def predict(self,x):
      raise NotImplementedError()