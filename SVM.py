import numpy as np
import pandas as pd

import sklearn
data=pd.read_csv("DSL-StrongPasswordData.csv")
data=data.drop(["sessionIndex","rep"],axis=1)
from sklearn import preprocessing
le = preprocessing.LabelEncoder()
data['subject'] = le.fit_transform(data['subject'])

print(data.head())
x=data.iloc[:,1:100].values
y=data.iloc[:,0:1].values

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

xtrain,xtest,ytrain,ytest=train_test_split(x,y,test_size=0.1)

from sklearn.svm import SVC
clf = SVC(kernel='rbf')
clf.fit(xtrain,ytrain)
ypred=clf.predict(xtest)
print(xtest[0])
print(accuracy_score(ytest,ypred) )

print("edi"+" .tie5Roanl")
#.tie5Roanl 

