"""Staged hyperparameter search for NeuralNet.py, scored on a validation split (the test set is never used).

Usage: python hpsearch.py STAGE   (0 = preprocessing, 1 = architecture, 2 = regularisation, 3 = optimiser)
"""
import os, sys, json, itertools, time
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
import numpy as np, pandas as pd, keras
from keras import layers
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

d = pd.read_csv("DSL-StrongPasswordData.csv")
x = d.iloc[:, 3:34].values.astype("float32")
y = pd.factorize(d["subject"])[0]
# Same held-out test split as NeuralNet.py; tune only on a val split carved from train.
xtr, xte, ytr, yte = train_test_split(x, y, test_size=0.1, random_state=42, stratify=y)
xtr, xva, ytr, yva = train_test_split(xtr, ytr, test_size=0.1111, random_state=0, stratify=ytr)

def prep(kind):
    if kind == "none": return xtr, xva
    f = (lambda a: np.log(a + 1.0)) if kind == "log" else (lambda a: a)   # UD can be negative; min ~ -0.2
    s = StandardScaler().fit(f(xtr)); return s.transform(f(xtr)), s.transform(f(xva))

def run(c, seed):
    keras.utils.set_random_seed(seed)
    a, b = prep(c["prep"])
    m = keras.Sequential([keras.Input((31,))])
    for w in c["layers"]:
        m.add(layers.Dense(w))
        if c["bn"]: m.add(layers.BatchNormalization())
        m.add(layers.Activation("relu"))
        if c["drop"]: m.add(layers.Dropout(c["drop"]))
    m.add(layers.Dense(51, activation="softmax"))
    m.compile(optimizer=keras.optimizers.Adam(c["lr"]), loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    cb = [keras.callbacks.EarlyStopping("val_accuracy", patience=30, restore_best_weights=True),
          keras.callbacks.ReduceLROnPlateau("val_loss", factor=0.5, patience=10)] if c["es"] else []
    h = m.fit(a, ytr, epochs=c["epochs"], batch_size=c["bs"], validation_data=(b, yva), verbose=0, callbacks=cb)
    return m.evaluate(b, yva, verbose=0)[1], len(h.history["loss"])

def score(c, seeds=(1, 2)):
    t = time.time(); r = [run(c, s) for s in seeds]
    acc = float(np.mean([v for v, _ in r]))
    print(f"{acc:.4f} ±{np.std([v for v,_ in r]):.4f} ep={[e for _,e in r]} {time.time()-t:4.0f}s {json.dumps(c)}", flush=True)
    return acc

base = dict(prep="none", layers=[16, 12], bn=False, drop=0.0, lr=1e-3, bs=64, epochs=100, es=False)
stage = sys.argv[1]
if stage == "0":   # baseline (current NeuralNet.py) + preprocessing
    score(base)
    for p in ["std", "log"]: score({**base, "prep": p})
if stage == "1":   # architecture, log prep, early stopping
    b = {**base, "prep": "log", "epochs": 400, "es": True}
    for L in [[16, 12], [64], [128, 64], [256, 128], [256, 256], [512, 256], [256, 256, 128], [512, 512, 256]]:
        score({**b, "layers": L})
if stage == "2":   # regularisation
    b = {**base, "prep": "log", "epochs": 400, "es": True}
    for L in [[512, 256], [512, 512, 256]]:
        for bn, dr in itertools.product([False, True], [0.2, 0.35, 0.5]):
            score({**b, "layers": L, "bn": bn, "drop": dr})
if stage == "3":   # optimiser
    b = {**base, "prep": "log", "epochs": 400, "es": True, "layers": [512, 256], "drop": 0.35}
    for lr, bs in itertools.product([3e-4, 1e-3, 3e-3], [32, 64, 128]):
        if (lr, bs) != (1e-3, 64): score({**b, "lr": lr, "bs": bs})
    score({**b, "layers": [1024, 512]})
