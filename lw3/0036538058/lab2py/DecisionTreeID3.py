from DecisionTreeInterface import DecisionTree
from Dataset import TrainDataset, TestDataset, Leaf,Node
from metrics import informationGain,entropy
import numpy as np

class DecisionTreeID3(DecisionTree):
   def __init__(self,max_depth:int=None):
      self.max_depth = max_depth
      self.tree = {}
   def fit(self,train_dataset : TrainDataset):
      self.tree = self.id3(D = train_dataset,D_parent=train_dataset,X=train_dataset.get_feature_names(),y=train_dataset.get_labels())
   
   def id3(self,D:TrainDataset,D_parent:TrainDataset,X:list,y:list):
      if D is None or len(D.get_data()) == 0:
         v = D_parent.most_common_label()
         return Leaf(v)
      
      v = D.most_common_label()
      data = D.get_data()
      mask = (D.get_labels()==v)
      if X is None  or len(data)==len(data[mask]):
         return Leaf(v)

      x = X[np.argmax(informationGain(D,feature)[1] for feature in X)]
      
      subtrees = []
      V = np.unique(data[x])
      for v in V:
         new_X = [feature for feature in X if feature != x]
         t = self.id3(D = D.filter(x,v),D_parent=D,X = new_X,y=y)
         subtrees.append((v,t))
      return Node(x,subtrees)
   
   def predict(self,test_dataset:TestDataset):
      return 1
      data = test_dataset.get_data()
      labels = []
      for i in range(len(data)):
         node = self.tree
         while not isinstance(node,Leaf):
            feature = node.feature
            value = data[feature].iloc[i]
            for (v,t) in node.subtrees:
               if v == value:
                  node = t
                  break
         labels.append(node.v)
      return labels
#output: level:feature_name=feature_value