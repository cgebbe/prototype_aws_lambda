import os
import pathlib
import numpy as np
import pandas as pd
from sklearn import preprocessing

DATA_PATH = pathlib.Path(__file__).parents[1] / "data"


class _Scaler:
    def __init__(
        self, reference_data_path=DATA_PATH / "historical_sensor_data.csv"
    ) -> None:
        df = read_csv(reference_data_path)
        x = df[["sensor_1", "sensor_2"]].values

        self.scaler = preprocessing.StandardScaler()
        self.scaler.fit(x)

    def transform(self, x: np.ndarray) -> np.ndarray:
        return self.scaler.transform(x)


def read_csv(path: os.PathLike) -> pd.DataFrame:
    return pd.read_csv(path, sep=",")


def to_csv(df: pd.DataFrame, path: os.PathLike) -> None:
    df.to_csv(path, sep=",", header=True, index=False)


def read_dataset(path: os.PathLike):
    df = read_csv(path)
    X_unscaled = df[["sensor_1", "sensor_2"]].values
    X = _Scaler().transform(X_unscaled)

    y = df[["label"]].values if "label" in df else None
    return X, y
