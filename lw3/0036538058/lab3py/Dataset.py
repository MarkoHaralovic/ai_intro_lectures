from abc import ABC, abstractmethod
import pandas as pd

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
      v_c = self.get_labels().value_counts()
      max_count = v_c.max()
      most_common = v_c[v_c == max_count].index
      return sorted(most_common)[0]
   
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
   
class Node:
   def __init__(self,depth, feature, subtrees):
        self.depth=depth
        self.feature = feature
        self.subtrees = subtrees
   def str_to_child(self):
      for child in self.subtrees:
         self.subtrees.parent_value = f"{self.depth}:{self.feature}={self.feature}"
   def __str__(self):
        subtree_str = "\n".join(f"{self.depth}:{self.feature}={v} {str(t)}" for v, t in self.subtrees)
        return f"{subtree_str}"
