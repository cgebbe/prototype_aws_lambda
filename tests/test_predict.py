import pathlib
import numpy as np
from sklearn import metrics

from src import predict, preprocess


def test_predict_yields_reproducible_result():
    # FIXME: fixed model should be saved in "test" folder (but trying to minimize size)
    model_path = pathlib.Path(__file__).parents[1] / "src" / "model.pickle"
    expected_probabilites = np.load(
        pathlib.Path(__file__).parent / "expected_probabilites.npy"
    )

    test_data_path = preprocess.DATA_PATH / "val.csv"
    X, _ = preprocess.read_dataset(test_data_path)

    predictor = predict.Predictor(model_path)
    probabilities = predictor.predict(
        x=X,
        return_probabilities=True,
    )
    np.testing.assert_almost_equal(probabilities, expected_probabilites)

    y_pred = np.round(probabilities)
    _, y_true = preprocess.read_dataset(test_data_path)
    accuracy = metrics.accuracy_score(y_true=y_true, y_pred=y_pred)
    np.testing.assert_equal(
        accuracy, 0.9777777777777777
    )  # same validation accuracy as from training
