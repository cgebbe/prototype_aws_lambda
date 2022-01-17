from typing import Dict
import json
import numpy as np
import pathlib
from src import predict

_predictor = predict.Predictor(
    model_path=pathlib.Path(__file__).parent / "model.pickle"
)


def _preprocess(event: Dict) -> np.ndarray:
    lst1 = json.loads(event["sensor_1"])
    lst2 = json.loads(event["sensor_2"])
    x = np.vstack([np.array(lst1), np.array(lst2)]).T
    return x


def _postprocess(result: np.ndarray) -> Dict:
    return {"class": result.tolist()}


def handler(event: Dict, context) -> Dict:
    """handler invoked by AWS Lambda function

    event: JSON formatted document, see
    https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-concepts.html#gettingstarted-concepts-event
    context: ?
    """
    input_array = _preprocess(event)
    output_array = _predictor.predict(input_array)
    output_dict = _postprocess(output_array)
    return output_dict
