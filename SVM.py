import pandas as pd
from sklearn import preprocessing
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

data = pd.read_csv("DSL-StrongPasswordData.csv")
data = data.drop(["sessionIndex", "rep"], axis=1)
le = preprocessing.LabelEncoder()
data["subject"] = le.fit_transform(data["subject"])

print(data.head())
x = data.iloc[:, 1:].values  # 31 timing features
y = data["subject"].values

xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.1, random_state=42, stratify=y)

clf = SVC(kernel="rbf")
clf.fit(xtrain, ytrain)
ypred = clf.predict(xtest)
print("SVM test accuracy:", accuracy_score(ytest, ypred))
