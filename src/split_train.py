import src.preprocess as preprocess
import pathlib
from sklearn import model_selection

if __name__ == "__main__":
    data_path = preprocess.DATA_PATH
    train_csv = data_path / "historical_sensor_data.csv"
    assert train_csv.exists

    df = preprocess.read_csv(train_csv)
    index_train, index_val = model_selection.train_test_split(
        df.index, test_size=0.3, random_state=99
    )

    preprocess.to_csv(df.loc[index_train, :], data_path / "train.csv")
    preprocess.to_csv(df.loc[index_val, :], data_path / "val.csv")
