from src import app
import numpy as np

_EVENT = {
    "sensor_1": "[1,2.0,3]",
    "sensor_2": "[-1,0,1]",
}


def test_handler_works():
    dct = app.handler(event=_EVENT, context=None)
    assert isinstance(dct, dict)

    excepted_dct = {"class": [1.0, 1.0, 1.0]}
    np.testing.assert_equal(dct, excepted_dct)
