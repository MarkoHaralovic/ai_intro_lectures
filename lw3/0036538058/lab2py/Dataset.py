from abc import ABC, abstractmethod
import pandas as pd
import numpy as np

class Dataset(ABC):
   @abstractmethod
   def __init__(self,data_path:str,*args,**kwargs):
      raise NotImplementedError()
   @abstractmethod
   def get_data(self):
      raise NotImplementedError()
   @abstractmethod
   def get_labels(self):
      raise NotImplementedError()
   @abstractmethod
   def get_features(self):
      raise NotImplementedError()
   @abstractmethod
   def get_target(self):
      raise NotImplementedError()
   @abstractmethod
   def get_feature_names(self):
      raise NotImplementedError()
   @abstractmethod
   def __len__(self):
      raise NotImplementedError()

   
class TrainDataset(Dataset):
   def __init__(self,data_path:str):
      self.data_path = data_path
      self.data = pd.read_csv(self.data_path,encoding='utf-8')
      self.features = self.data.columns[:-1]
      self.target = self.data.columns[-1]
   def get_data(self):
      return self.data
   def get_labels(self):
      return self.data.iloc[:, -1]
   def get_features(self):
      return self.data.iloc[:,:-1]
   def get_feature_names(self):
      return self.features
   def get_target(self):
      return self.target
   def __len__(self):
      return len(self.data)
   def filter(self,feature,feature_value):
      new_ds = TrainDataset(self.data_path)
      new_ds.data = self.data[self.data[feature] == feature_value]
      return new_ds
   def most_common_label(self):
      return self.data.value_counts().idxmax()[-1] if len(self.data) else 0
   
class TestDataset(Dataset):
   def __init__(self,data_path:str):
      self.data_path = data_path
      self.data = pd.read_csv(self.data_path,encoding='utf-8')
      self.features = self.data.columns[:-1]
      self.target = self.data.columns[-1]
   def get_data(self):
      return self.data
   def get_labels(self):
      return self.data.iloc[:, -1]
   def get_features(self):
      return self.data.iloc[:,:-1]
   def get_feature_names(self):
      return self.features
   def get_target(self):
      return self.target
   def __len__(self):
      return len(self.data)
   def filter(self,feature,feature_value):
      self.data = self.data[self.data[feature] == feature_value]
      return self
   
class Leaf:
   def __init__(self,v):
      self.v = v
   def __str__(self):
      return str(self.v)
   def print(self):
      print(f"Leaf with value : {self.v}")
   
class Node:
   def __init__(self,depth, feature, subtrees):
        self.depth=depth
        self.feature = feature
        self.subtrees = subtrees
   def __str__(self):
        subtree_str = "\n".join(f"{self.depth + 1}:{self.feature}:{v}={str(t)}" for v, t in self.subtrees)
        return f"{self.depth}:{self.feature}\n{subtree_str}"
