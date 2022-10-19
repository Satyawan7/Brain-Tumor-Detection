# -*- coding: utf-8 -*-
"""Brain_tumor_detection_SVM.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rjrX_j-JuxgrN_Dq5a8E7HiRXA9G3Wlq
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from google.colab import drive

drive.mount('/content/drive')

import os
path = os.listdir('/content/drive/MyDrive/Br35H-Mask-RCNN/TRAIN')
classes = {'no':0, 'yes':1}

import cv2
X = []
Y = []
for cls in classes:
    pth = '/content/drive/MyDrive/Br35H-Mask-RCNN/TRAIN/'+cls
    for j in os.listdir(pth):
        img = cv2.imread(pth+'/'+j, 0)
        img = cv2.resize(img, (200,200))
        X.append(img)
        Y.append(classes[cls])

X = np.array(X)
Y = np.array(Y)
X_updated = X.reshape(len(X), -1)

np.unique(Y)

pd.Series(Y).value_counts()

X.shape, X_updated.shape

#Visualise the data
plt.imshow(X[0], cmap='gray')

#Prepare data
X_updated = X.reshape(len(X), -1)
X_updated.shape

xtrain, xtest, ytrain, ytest = train_test_split(X_updated, Y, random_state=10,
 test_size=.20)

xtrain.shape, xtest.shape

#Feature Scaling
print(xtrain.max(), xtrain.min())
print(xtest.max(), xtest.min())
xtrain = xtrain/255
xtest = xtest/255
print(xtrain.max(), xtrain.min())
print(xtest.max(), xtest.min())

from sklearn.preprocessing import OneHotEncoder
oneh = OneHotEncoder(handle_unknown="ignore")

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

import warnings
warnings.filterwarnings('ignore')
lg = LogisticRegression(C=0.1)
lg.fit(xtrain, ytrain)

sv = SVC()
sv.fit(xtrain, ytrain)

#Evaluation
print("Training Score:", lg.score(xtrain, ytrain))
print("Testing Score:", lg.score(xtest, ytest))

print("Training Score:", sv.score(xtrain, ytrain))
print("Testing Score:", sv.score(xtest, ytest))

pred = sv.predict(xtest)

misclassified=np.where(ytest!=pred)
misclassified

print("Total Misclassified Samples: ",len(misclassified[0]))
print(pred[36],ytest[36])

dec = {0:'No', 1:'yes'}

plt.figure(figsize=(12,8))
p = os.listdir('/content/drive/MyDrive/Br35H-Mask-RCNN/TRAIN')
c=1
for i in os.listdir('/content/drive/MyDrive/Br35H-Mask-RCNN/TRAIN/no/')[:9]:
 plt.subplot(3,3,c)
 
 img = cv2.imread('/content/drive/MyDrive/Br35H-Mask-RCNN/TRAIN/no/'+i,0)
 img1 = cv2.resize(img, (200,200))
 img1 = img1.reshape(1,-1)/255
 p = sv.predict(img1)
 plt.title(dec[p[0]])
 plt.imshow(img, cmap='gray')
 plt.axis('off')
 c+=1

plt.figure(figsize=(12,8))
p = os.listdir('/content/drive/MyDrive/Br35H-Mask-RCNN/TRAIN')
c=1
for i in os.listdir('/content/drive/MyDrive/Br35H-Mask-RCNN/TRAIN/yes/')[:16]:
 plt.subplot(4,4,c)
 
 img = cv2.imread('/content/drive/MyDrive/Br35H-Mask-RCNN/TRAIN/yes/'+i,0)
 img1 = cv2.resize(img, (200,200))
 img1 = img1.reshape(1,-1)/255
 p = sv.predict(img1)
 plt.title(dec[p[0]])
 plt.imshow(img, cmap='gray')
 plt.axis('off')
 c+=1