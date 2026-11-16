import matplotlib.pyplot as plt
import pandas as pd
from keras.layers import Dense
from keras.models import Sequential
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

dataset = pd.read_csv("DSL-StrongPasswordData.csv")
print(dataset.head(10))
x = dataset.iloc[:, 3:34].values  # 31 timing features
y = dataset.iloc[:, 0:1].values   # subject id

print(x.shape)
ohe = OneHotEncoder()
y = ohe.fit_transform(y).toarray()
print(y.shape)

# Hold out a stratified test set so the reported accuracy is on unseen data.
# (Keras' validation_split would take the last rows, i.e. only the last subjects.)
xtrain, xtest, ytrain, ytest = train_test_split(
    x, y, test_size=0.1, random_state=42, stratify=y.argmax(axis=1))

model = Sequential()
model.add(Dense(16, input_dim=x.shape[1], activation="relu"))
model.add(Dense(12, activation="relu"))
model.add(Dense(y.shape[1], activation="softmax"))

model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

history = model.fit(xtrain, ytrain, epochs=100, batch_size=64, validation_data=(xtest, ytest))

_, test_acc = model.evaluate(xtest, ytest, verbose=0)
print("Neural network test accuracy:", test_acc)

# Metric key is "accuracy" in TF2 / Keras 3, "acc" in old Keras.
acc_key = "accuracy" if "accuracy" in history.history else "acc"
plt.plot(history.history[acc_key])
plt.plot(history.history["val_" + acc_key])
plt.title("Model accuracy")
plt.ylabel("Accuracy")
plt.xlabel("Epoch")
plt.legend(["Train", "Test"], loc="upper left")
plt.show()
