import pathlib
import numpy as np
import pandas as pd

from src import preprocess


def test_dataset_roundtrip(tmp_path):
    dataset_path = pathlib.Path(__file__).parent / "dataset.csv"
    assert dataset_path.exists()

    tmp_file = tmp_path / "df.csv"
    direct = preprocess.read_csv(dataset_path)
    preprocess.to_csv(direct, tmp_file)

    roundtrip = preprocess.read_csv(tmp_file)
    pd.testing.assert_frame_equal(direct, roundtrip)
