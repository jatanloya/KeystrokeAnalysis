# Keystroke Analysis for Authentication

A system for analysing keystroke dynamics to authenticate users based on their inherent typing behaviour.

We built models using an SVM, a Manhattan (scaled) detector and a neural network,
and a basic GUI for generating and retrieving keystroke data.

Our neural network reaches about 95% accuracy on a held-out test set (the SVM reaches about 79%), and the scaled Manhattan detector has an average Equal Error Rate of 0.096.

The models use the [CMU Keystroke Dynamics Benchmark dataset](https://www.cs.cmu.edu/~keystroke/)
(`DSL-StrongPasswordData.csv`, included in this repo).

## Setup

```bash
pip install -r requirements.txt
```

## Usage

Run the scripts from the repository root (they read `DSL-StrongPasswordData.csv` from the working directory):

| Script | What it does |
| --- | --- |
| `python Manhatton_scale_detector.py` | Average Equal Error Rate (EER) of the scaled Manhattan anomaly detector across all subjects |
| `python SVM.py` | Trains an RBF SVM to identify the subject and prints test accuracy |
| `python NeuralNet.py` | Trains a dense network (log-scaled features, 512→256 with dropout, early stopping) to identify the subject, prints test accuracy and plots accuracy per epoch |
| `python DataGen.py` | Records key-press timestamps while you type a password (needs keyboard-monitoring permission on macOS) |
| `python GUI/logger.py`, `python GUI/login.py` | Basic Tkinter GUIs for entering a password and a demo login screen |

## References
https://www.cs.cmu.edu/~keystroke/

This is a very comprehensive source for anyone who wants to try out keystroke analysis.

https://www.cs.cmu.edu/~keystroke/KillourhyMaxion09.pdf

The above research paper compares various anomaly detection algorithms and how they fare for this purpose.
