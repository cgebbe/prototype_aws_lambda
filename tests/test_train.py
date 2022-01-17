import yaml
import numpy as np

from src import train, preprocess


def test_train_yields_reproducible_results(tmp_path):
    train.train(
        train_data_path=preprocess.DATA_PATH / "train.csv",
        validation_data_path=preprocess.DATA_PATH / "val.csv",
        log_directory=tmp_path,
    )

    with open(tmp_path / "metrics.yml", "r") as f:
        dct = yaml.safe_load(f)

    np.testing.assert_equal(dct["train_accuracy"], 0.9704761904761905)
    np.testing.assert_equal(dct["vaild_accuracy"], 0.9777777777777777)
