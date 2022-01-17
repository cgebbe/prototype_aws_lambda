import os
from datetime import datetime

import pathlib
import numpy as np
from sklearn.gaussian_process.kernels import RBF
from sklearn.gaussian_process import GaussianProcessClassifier
import pickle
import yaml

from src import preprocess

np.random.seed(0)  # for reproducible trainings


def train(
    train_data_path: os.PathLike,
    validation_data_path: os.PathLike,
    log_directory: os.PathLike = (
        pathlib.Path("logs") / datetime.now().strftime("%Y%m%d_%H%M%S")
    ),
):
    """Train and evaluate a model"""
    X_train, y_train = preprocess.read_dataset(train_data_path)
    X_test, y_test = preprocess.read_dataset(validation_data_path)

    clf = GaussianProcessClassifier(1.0 * RBF(1.0))
    clf.fit(X_train, y_train.ravel())

    log_directory = pathlib.Path(log_directory)
    log_directory.mkdir(exist_ok=True)
    with open(log_directory / "model.pickle", "wb") as f:
        pickle.dump(clf, f)

    metrics = {}
    for X, y, subset_name in [(X_train, y_train, "train"), (X_test, y_test, "vaild")]:
        metrics[f"{subset_name}_accuracy"] = float(clf.score(X, y))
    with open(log_directory / "metrics.yml", "w") as f2:
        yaml.dump(metrics, f2)  # type: ignore
