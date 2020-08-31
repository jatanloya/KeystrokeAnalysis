import pandas as pd
import numpy as np
import keras
import tensorflow
from keras.models import Sequential
from keras.layers.core import Dense
import matplotlib.pyplot as plt


dataset = pd.read_csv("DSL-StrongPasswordData.csv") 
print(dataset.head(10))
x=dataset.iloc[:,3:34].values
y=dataset.iloc[:,0:1].values

print(x.shape)
#print(dataset["standard"].unique().tolist())
from sklearn.preprocessing import OneHotEncoder
ohe = OneHotEncoder()
y = ohe.fit_transform(y).toarray()
print(y.shape)


model = Sequential()
model.add(Dense(16, input_dim=31, activation="relu"))
model.add(Dense(12, activation="relu"))
model.add(Dense(51, activation="softmax"))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

history = model.fit(x, y, epochs=100, batch_size=64)


plt.plot(history.history['acc'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()
#completed
