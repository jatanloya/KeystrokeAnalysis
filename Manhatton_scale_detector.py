import numpy as np
import pandas

from EER import evaluateEER

np.set_printoptions(suppress=True)


class ManhattanScaledDetector:
    # Same as the plain Manhattan detector; only training() differs (it also
    # computes the per-feature mean absolute deviation used for scaling).

    def __init__(self, data, subjects):
        self.data = data
        self.subjects = subjects
        self.user_scores = []
        self.imposter_scores = []
        self.mean_vector = []
        self.mad_vector = []

    def training(self):
        self.mean_vector = self.train.mean().values
        # Mean absolute deviation of each feature (DataFrame.mad() was removed in pandas 2.0).
        self.mad_vector = (self.train - self.train.mean()).abs().mean().values

    def _score(self, samples):
        return list((np.abs(samples.values - self.mean_vector) / self.mad_vector).sum(axis=1))

    def testing(self):
        self.user_scores = self._score(self.test_genuine)
        self.imposter_scores = self._score(self.test_imposter)

    def evaluate(self):
        eers = []

        for subject in self.subjects:
            genuine_user_data = self.data.loc[self.data.subject == subject,
                                              "H.period":"H.Return"]
            imposter_data = self.data.loc[self.data.subject != subject, :]

            # First 200 reps train, remaining 200 test; first 5 reps of every
            # other subject are the imposter samples (Killourhy & Maxion 2009).
            self.train = genuine_user_data[:200]
            self.test_genuine = genuine_user_data[200:]
            self.test_imposter = imposter_data.groupby("subject"). \
                head(5).loc[:, "H.period":"H.Return"]

            self.training()
            self.testing()
            eers.append(evaluateEER(self.user_scores, self.imposter_scores))
        return np.mean(eers)


if __name__ == "__main__":
    path = "DSL-StrongPasswordData.csv"
    data = pandas.read_csv(path)
    subjects = data["subject"].unique()
    print("average EER for Manhattan Scaled detector:")
    print(ManhattanScaledDetector(data, subjects).evaluate())
