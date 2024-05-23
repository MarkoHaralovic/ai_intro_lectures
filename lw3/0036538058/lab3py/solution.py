import argparse
import itertools
from DecisionTreeID3 import DecisionTreeID3
from Dataset import TrainDataset, TestDataset
from metrics import accuracy, confusionMatrix

def parse_command_line():
   parser = argparse.ArgumentParser()
   parser.add_argument('path_to_train_set',type=str,help="Path to the file with the training set.")
   parser.add_argument('path_to_test_set',type=str,help="Path to the file with the testing set.")
   parser.add_argument('tree_depth', nargs='?', type=int, default=-1, help="The maximum depth of the decision tree.")
   args = parser.parse_args()
   return args

def main():
   args = parse_command_line()

   train_set_path, test_set_path, tree_depth = args.path_to_train_set,args.path_to_test_set,args.tree_depth
   if tree_depth == -1:
      model = DecisionTreeID3()
   else:
      model = DecisionTreeID3(tree_depth)
   train_dataset = TrainDataset(train_set_path)
   test_dataset = TrainDataset(test_set_path)

   model.fit(train_dataset)
   predictions = model.predict(test_dataset)
   
   print("[BRANCHES]:")
   model.print_tree()
   
   preds = "".join(str(prediction) + " " for prediction in predictions)
   print(f"[PREDICTIONS]: {preds}")
   print(f"[ACCURACY]: {accuracy(predictions,test_dataset.get_labels())}")
   
   print("[CONFUSION_MATRIX]:")
   CM = confusionMatrix(predictions,test_dataset.get_labels())
   for row in CM:
      print("".join(str(int(cell)) + " " for cell in row))
   
if __name__ == '__main__':
   main()