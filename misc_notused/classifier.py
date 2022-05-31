#pierre amir


import numpy as np
from sklearn import preprocessing
import random
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from collections import Counter
    
dataset_train = np.loadtxt('training.txt', delimiter=",")
print(dataset_train.shape,"train_shape")
dataset_test = np.loadtxt('testing.txt', delimiter=",")
print(dataset_test.shape,"test_shape")

X_train = dataset_train[:,0:169]
Y_train = dataset_train[:,170]     

X_test = dataset_test[:,0:169]
Y_test = dataset_test[:,170]
print(Y_test)


print("initially unbalanced classes : ")
print(sorted(Counter(Y_train).items()))

#############################TRAIN##############################################


print("SUPPORT VECTOR MACHINES")
clf_name = "svc"
resultFolder = "/home/sherlock/Internship@iit/exudate-detection/"+clf_name+"_results-exudates/"
clf = SVC(kernel = 'linear')
clf.fit(X_train, Y_train)
Y_predicted = clf.predict(X_test)
print("accuracy")
print(accuracy_score(Y_test, Y_predicted))
print("confusion matrix")
print (confusion_matrix(Y_test,Y_predicted))
# writeResults(DestinationFolder,resultFolder,name_array,clf_name,Y_predicted)

print("KNN_ NEAREST NEIGHBOURS")
clf_name = "knn"
resultFolder = "/home/sherlock/Internship@iit/exudate-detection/"+clf_name+"_results-exudates/"
clf = KNeighborsClassifier(n_neighbors = 10)
clf.fit(X_train, Y_train)
Y_predicted = clf.predict(X_test)
print("accuracy")
print(accuracy_score(Y_test, Y_predicted))
print("confusion matrix")
print (confusion_matrix(Y_test,Y_predicted))
# writeResults(DestinationFolder,resultFolder,name_array,clf_name,Y_predicted)

#############################TEST##############################################

print("SUPPORT VECTOR MACHINES")
clf_name = "svc"
resultFolder = "/home/sherlock/Internship@iit/exudate-detection/"+clf_name+"_BAL_results-exudates/"
clf = SVC(kernel = 'linear')
clf.fit(X_resampled, Y_resampled)
Y_predicted = clf.predict(X_test)
print("accuracy")
print(accuracy_score(Y_test, Y_predicted))
print("confusion matrix")
print (confusion_matrix(Y_test,Y_predicted))
writeResults(DestinationFolder,resultFolder,name_array,clf_name,Y_predicted)

print("KNN_ NEAREST NEIGHBOURS")
clf_name = "knn"
resultFolder = "/home/sherlock/Internship@iit/exudate-detection/"+clf_name+"_BAL_results-exudates/"
clf = KNeighborsClassifier(n_neighbors = 10)
clf.fit(X_resampled, Y_resampled)
Y_predicted = clf.predict(X_test)
print("accuracy")
print(accuracy_score(Y_test, Y_predicted))
print("confusion matrix")
print (confusion_matrix(Y_test,Y_predicted))
writeResults(DestinationFolder,resultFolder,name_array,clf_name,Y_predicted)
