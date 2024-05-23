import math
from Dataset import Dataset,TrainDataset,TestDataset

def accuracy(predictions, labels):
    TP = sum(p==l for p,l in zip(predictions,labels))
    return "{:.5f}".format(round(TP/len(labels),5))

def confusionMatrix(predictions, labels):
    unique_labels = sorted(list(set(labels)))
    matrix = [[0 for i in range(len(unique_labels))] for j in range(len(unique_labels))]
    for i in range(len(unique_labels)):
        for j in range(len(unique_labels)):
            matrix[i][j] = sum([1 for pred, label in zip(predictions, labels) if label == unique_labels[i] and pred == unique_labels[j]])
    return matrix

def entropy(dataset: Dataset, feature: str, feature_value=None):
    data = dataset.get_data()
    labels = dataset.get_labels()

    if feature_value is not None:
        mask = data[feature] == feature_value
        data = data[mask]
        labels = labels[mask]

    if len(labels) == 0:
        return 0  

    unique_labels = labels.unique()

    _entropy = 0
    for label in unique_labels:
        p = sum(labels == label) / len(labels)
        _entropy += -p * math.log2(p)
    
    return _entropy,len(labels)

def informationGain(dataset:Dataset,parentNode:str,childNodes:list):
    parentNodeEntropy,_ = entropy(dataset,parentNode)
    childNodes = sorted(childNodes)
    childEntropies = [entropy(dataset,parentNode,child) for child in childNodes]
    ig = parentNodeEntropy - sum([childEntropy[0] * childEntropy[1] / len(dataset) for childEntropy in childEntropies])
    lowest_entropy_feature = min([childEntropy[0] for childEntropy in enumerate(childEntropies)])
    return round(ig,4),childNodes[lowest_entropy_feature] 

train_set_path = r"C:\FER\6TH SEMESTER\INTRO_TO_AI\autograder\data\lab3\files\volleyball.csv"
train_dataset = TrainDataset(train_set_path)

# print(entropy(train_dataset,'temperature','comfortable'))
# print(entropy(train_dataset,'temperature','hot'))
# print(entropy(train_dataset,'temperature','cold'))

# print(informationGain(train_dataset,'temperature',['comfortable','hot','cold']))

# print(train_dataset.most_common_label())