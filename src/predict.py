import pickle
import numpy as np
from sklearn.gaussian_process import GaussianProcessClassifier


class Predictor:
    def __init__(self, model_path) -> None:
        with open(model_path, "rb") as f:
            self.clf: GaussianProcessClassifier = pickle.load(f)

    def predict(self, x: np.ndarray, return_probabilities=False) -> np.ndarray:
        assert (
            x.ndim == 2 and x.shape[-1] == 2
        ), f"Expected input shape (N,2) but received {x.shape}"
        all_probabilites = self.clf.predict_proba(x)
        true_prob = all_probabilites[:, 1].ravel()
        if return_probabilities:
            return true_prob
        return np.round(true_prob)
