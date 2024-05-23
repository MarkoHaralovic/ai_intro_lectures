from DecisionTreeInterface import DecisionTree
from Dataset import TrainDataset, TestDataset, Leaf,Node
from metrics import informationGain,entropy

class DecisionTreeID3(DecisionTree):
   def __init__(self,max_depth:int=None):
      self.max_depth = max_depth
      self.tree = {}
      
   def fit(self,train_dataset : TrainDataset):
      self.tree = self.id3(D = train_dataset,D_parent=train_dataset,X=train_dataset.get_feature_names(),y=train_dataset.get_labels(),depth=0)
   
   def id3(self,D:TrainDataset,D_parent:TrainDataset,X:list,y:list,depth:int):
      if D is None or len(D.get_data()) == 0:
         v = D_parent.most_common_label()
         return Leaf(v)
      
      if self.max_depth is not None and depth == self.max_depth:
         v = D.most_common_label()
         return Leaf(v)
     
      v = D.most_common_label()
      data = D.get_data()
      mask = (D.get_labels()==v)
      if X is None  or len(data)==len(data[mask]):
         return Leaf(v)
      IGS = [informationGain(D,feature,D.get_features()[feature].unique())[0] for feature in X]
      if len(IGS)==0:
         return Leaf(v)
      max_ig = max(IGS)
      max_ig_index = IGS.index(max_ig)
      x = X[max_ig_index]
      subtrees = []
      V = data[x].unique()
      for v in V:
         new_X = sorted([feature for feature in X if feature != x])
         t = self.id3(D = D.filter(x,v),D_parent=D,X = new_X,y=y,depth=depth+1)
         subtrees.append((v,t))
      return Node(depth+1,x,subtrees)
   
   def predict(self,test_dataset:TestDataset):
      data = test_dataset.get_features()
      labels = []
      for i in range(len(data)):
         node = self.tree 
         while not isinstance(node,Leaf):
            feature = node.feature
            value = data[feature].iloc[i]
            if value not in [v for (v,t) in node.subtrees]:
               labels.append(test_dataset.most_common_label())
               break
            for (v,t) in node.subtrees:
               if v == value:
                  node = t
                  break
            if feature is None:
               labels.append(node.v)
         labels.append(node.v) if isinstance(node, Leaf) else None
      return labels
   def print_tree(self):
      if isinstance(self.tree, Leaf):
         print(self.tree)
      else:
         self._print_subtree(self.tree, "")

   def _print_subtree(self, node, prefix):
      if isinstance(node, Leaf):
         print(f"{prefix}{node.v}")
      else:
         for value, subtree in node.subtrees:
            new_prefix = f"{prefix}{node.depth}:{node.feature}={value} "
            self._print_subtree(subtree, new_prefix)
