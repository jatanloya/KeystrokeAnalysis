from sklearn.metrics import roc_curve
import numpy as np


def evaluateEER(user_scores, imposter_scores):
    """Equal Error Rate for anomaly scores (higher score = more likely an imposter)."""
    labels = [0] * len(user_scores) + [1] * len(imposter_scores)
    fpr, tpr, thresholds = roc_curve(labels, list(user_scores) + list(imposter_scores))
    missrates = 1 - tpr
    farates = fpr
    dists = missrates - farates
    # Indices into the full arrays (not the filtered sub-arrays) of the two ROC
    # points that bracket the crossing point missrate == farate.
    nonneg = np.flatnonzero(dists >= 0)
    neg = np.flatnonzero(dists < 0)
    idx1 = nonneg[np.argmin(dists[nonneg])]
    if neg.size == 0:
        return missrates[idx1]
    idx2 = neg[np.argmax(dists[neg])]
    x = [missrates[idx1], farates[idx1]]
    y = [missrates[idx2], farates[idx2]]
    # Linearly interpolate between x and y to where missrate == farate.
    a = (x[0] - x[1]) / (y[1] - x[1] - y[0] + x[0])
    eer = x[0] + a * (y[0] - x[0])
    return eer
