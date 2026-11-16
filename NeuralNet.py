import keras
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from keras import layers
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler

keras.utils.set_random_seed(1)

dataset = pd.read_csv("DSL-StrongPasswordData.csv")
print(dataset.head(10))
x = dataset.iloc[:, 3:34].values  # 31 timing features
y = dataset.iloc[:, 0:1].values   # subject id

print(x.shape)
ohe = OneHotEncoder()
y = ohe.fit_transform(y).toarray()
print(y.shape)

# Stratified splits: 80% train, 10% validation (early stopping), 10% held-out test.
# (Keras' validation_split would take the last rows, i.e. only the last subjects.)
xtrain, xtest, ytrain, ytest = train_test_split(
    x, y, test_size=0.1, random_state=42, stratify=y.argmax(axis=1))
xtrain, xval, ytrain, yval = train_test_split(
    xtrain, ytrain, test_size=1 / 9, random_state=0, stratify=ytrain.argmax(axis=1))

# Timings are right-skewed, so log-transform then standardise (fit on train only).
# log1p is safe: the up-down (UD) latencies can be negative but are always > -1 s.
scaler = StandardScaler().fit(np.log1p(xtrain))
xtrain, xval, xtest = (scaler.transform(np.log1p(a)) for a in (xtrain, xval, xtest))

model = keras.Sequential([
    keras.Input(shape=(x.shape[1],)),
    layers.Dense(512, activation="relu"),
    layers.Dropout(0.35),
    layers.Dense(256, activation="relu"),
    layers.Dropout(0.35),
    layers.Dense(y.shape[1], activation="softmax"),
])

model.compile(loss="categorical_crossentropy", optimizer=keras.optimizers.Adam(1e-3),
              metrics=["accuracy"])

callbacks = [
    keras.callbacks.EarlyStopping(monitor="val_accuracy", patience=30, restore_best_weights=True),
    keras.callbacks.ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=10),
]
history = model.fit(xtrain, ytrain, epochs=400, batch_size=128,
                    validation_data=(xval, yval), callbacks=callbacks)

_, test_acc = model.evaluate(xtest, ytest, verbose=0)
print("Neural network test accuracy:", test_acc)

plt.plot(history.history["accuracy"])
plt.plot(history.history["val_accuracy"])
plt.title("Model accuracy")
plt.ylabel("Accuracy")
plt.xlabel("Epoch")
plt.legend(["Train", "Validation"], loc="upper left")
plt.show()
