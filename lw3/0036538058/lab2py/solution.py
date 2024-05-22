import argparse
import itertools
from DecisionTreeID3 import DecisionTreeID3
from Dataset import TrainDataset, TestDataset

def parse_command_line():
   parser = argparse.ArgumentParser()
   parser.add_argument('path_to_train_set',type=str,help="Path to the file with the training set.")
   parser.add_argument('path_to_test_set',type=str,help="Path to the file with the testing set.")
   parser.add_argument('tree_depth',type=int,help="The maximum depth of the decision tree.")
   args = parser.parse_args()
   return args

def main():
   args = parse_command_line()

   train_set_path, test_set_path, tree_depth = args.path_to_train_set,args.path_to_test_set,args.tree_depth
   if tree_depth == None:
      model = DecisionTreeID3()
   else:
      model = DecisionTreeID3(tree_depth)
   train_dataset = TrainDataset(train_set_path)
   test_dataset = TrainDataset(test_set_path)
   # print(test_dataset.get_target())
   # print(test_dataset.get_features())
   model.fit(train_dataset)
   predictions = model.predict(test_dataset)
   
   # model.print_tree()
   
if __name__ == '__main__':
   main()