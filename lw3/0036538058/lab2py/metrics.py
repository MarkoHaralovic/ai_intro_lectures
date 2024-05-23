import numpy as np 
import pandas as pd 
import math
from numpy import argmax
from Dataset import Dataset,TrainDataset,TestDataset
from numpy import argmin

def accuracy(predictions, labels):
    return np.mean(predictions == labels)
 
def confusionMatrix(predictions, labels):
    labels = np.array(labels)
    predictions = np.array(predictions)
    unique_labels = np.unique(labels)
    matrix = np.zeros((len(unique_labels),len(unique_labels)))
    for i in range(len(unique_labels)):
        for j in range(len(unique_labels)):
            matrix[i,j] = np.sum((labels == unique_labels[i]) & (predictions == unique_labels[j]))
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

    unique_labels = np.unique(labels)

    _entropy = 0
    for label in unique_labels:
        p = np.sum(labels == label) / len(labels)
        _entropy += -p * math.log2(p)
    
    return _entropy,len(labels)

def informationGain(dataset:Dataset,parentNode:str,childNodes:list):
    parentNodeEntropy,_ = entropy(dataset,parentNode)
    childEntropies = [entropy(dataset,parentNode,child) for child in childNodes]
    ig = parentNodeEntropy - sum([childEntropy[0] * childEntropy[1] / len(dataset) for childEntropy in childEntropies])
    lowest_entropy_feature = argmin([childEntropy[0] for childEntropy in childEntropies])
    return round(ig,4),childNodes[lowest_entropy_feature] 

train_set_path = r"C:\FER\6TH SEMESTER\INTRO_TO_AI\autograder\data\lab3\files\volleyball.csv"
train_dataset = TrainDataset(train_set_path)

# print(entropy(train_dataset,'temperature','comfortable'))
# print(entropy(train_dataset,'temperature','hot'))
# print(entropy(train_dataset,'temperature','cold'))

print(informationGain(train_dataset,'temperature',['comfortable','hot','cold']))

print(train_dataset.most_common_label())