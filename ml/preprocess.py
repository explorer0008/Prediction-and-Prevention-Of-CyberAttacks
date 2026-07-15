import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler


class DataPreprocessor:

    def __init__(self, dataset_path):

        self.dataset_path = dataset_path

        self.dataframe = None

        self.scaler = StandardScaler()

        self.encoders = {}

    def load_dataset(self):

        if not os.path.exists(self.dataset_path):

            raise FileNotFoundError(self.dataset_path)

        self.dataframe = pd.read_csv(self.dataset_path)

        print(f"Dataset Loaded : {self.dataframe.shape}")

    def clean_dataset(self):

        self.dataframe.drop_duplicates(inplace=True)

        object_columns = self.dataframe.select_dtypes(

        include=["object", "string"]

        ).columns

        numeric_columns = self.dataframe.select_dtypes(

        exclude=["object", "string"]

        ).columns

        self.dataframe[object_columns] = self.dataframe[
        object_columns
        ].fillna("Unknown")

        self.dataframe[numeric_columns] = self.dataframe[
        numeric_columns
        ].fillna(0)

    def encode_features(self):

        categorical_columns = [

            "session_id",

            "protocol_type",

            "encryption_used",

            "browser_type"

        ]

        for column in categorical_columns:

            encoder = LabelEncoder()

            self.dataframe[column] = encoder.fit_transform(

                self.dataframe[column]

            )

            self.encoders[column] = encoder

    def split_dataset(self):

        X = self.dataframe.drop(

            "attack_detected",

            axis=1

        )

        y = self.dataframe["attack_detected"]

        return train_test_split(

            X,

            y,

            test_size=0.20,

            random_state=42,

            stratify=y

        )

    def scale_dataset(

        self,

        X_train,

        X_test

    ):

        X_train = self.scaler.fit_transform(

            X_train

        )

        X_test = self.scaler.transform(

            X_test

        )

        return X_train, X_test

    def save_artifacts(self):

        os.makedirs(

            "models",

            exist_ok=True

        )

        joblib.dump(

            self.scaler,

            "models/scaler.pkl"

        )

        joblib.dump(

            self.encoders,

            "models/encoders.pkl"

        )

    def preprocess(self):

        self.load_dataset()

        self.clean_dataset()

        self.encode_features()

        X_train, X_test, y_train, y_test = (

            self.split_dataset()

        )

        X_train, X_test = self.scale_dataset(

            X_train,

            X_test

        )

        self.save_artifacts()

        return (

            X_train,

            X_test,

            y_train,

            y_test

        )


if __name__ == "__main__":

    processor = DataPreprocessor(

        "datasets/cyber_attacks.csv"

    )

    processor.preprocess()

    print("Preprocessing Completed Successfully")