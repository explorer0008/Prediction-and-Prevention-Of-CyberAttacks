import joblib
import pandas as pd


class Predictor:

    def __init__(self):

        self.model = joblib.load("models/model.pkl")

        self.scaler = joblib.load("models/scaler.pkl")

        self.encoders = joblib.load("models/encoders.pkl")

    def load_dataset(self, dataset_path):

        dataframe = pd.read_csv(dataset_path)

        dataframe.drop_duplicates(inplace=True)

        object_columns = dataframe.select_dtypes(
            include=["object", "string"]
        ).columns

        numeric_columns = dataframe.select_dtypes(
            exclude=["object", "string"]
        ).columns

        dataframe[object_columns] = dataframe[
            object_columns
        ].fillna("Unknown")

        dataframe[numeric_columns] = dataframe[
            numeric_columns
        ].fillna(0)

        return dataframe

    def encode_features(self, dataframe):

        dataframe = dataframe.copy()

        for column, encoder in self.encoders.items():

            if column in dataframe.columns:

                dataframe[column] = encoder.transform(
                    dataframe[column]
                )

        return dataframe

    def preprocess(self, dataframe):

        dataframe = self.encode_features(
            dataframe
        )

        if "attack_detected" in dataframe.columns:

            dataframe = dataframe.drop(
                columns=["attack_detected"]
            )

        features = self.scaler.transform(
            dataframe
        )

        return features

    def predict(self, dataset_path):

        original_dataframe = self.load_dataset(
            dataset_path
        )

        features = self.preprocess(
            original_dataframe
        )

        predictions = self.model.predict(
            features
        )

        result = original_dataframe.copy()

        result["Prediction"] = predictions

        result["Prediction"] = result["Prediction"].map({

            0: "Benign",

            1: "Attack"

        })

        return result

    def attack_summary(self, dataframe):

        total_packets = len(dataframe)

        distribution = (

            dataframe["Prediction"]

            .value_counts()

            .to_dict()

        )

        attack_packets = distribution.get(

            "Attack",

            0

        )

        benign_packets = distribution.get(

            "Benign",

            0

        )

        threat_score = round(

            (attack_packets / total_packets) * 100,

            2

        )

        if threat_score >= 70:

            severity = "Critical"

        elif threat_score >= 40:

            severity = "High"

        elif threat_score >= 15:

            severity = "Medium"

        else:

            severity = "Low"

        return {

            "total_packets": total_packets,

            "attack_packets": attack_packets,

            "benign_packets": benign_packets,

            "threat_score": threat_score,

            "severity": severity,

            "attack_distribution": distribution

        }

    def run(self, dataset_path):

        predictions = self.predict(
            dataset_path
        )

        summary = self.attack_summary(
            predictions
        )

        return predictions, summary


if __name__ == "__main__":

    predictor = Predictor()

    predictions, summary = predictor.run(

        "datasets/cyber_attacks.csv"

    )

    print("\nPredictions\n")

    print(predictions.head())

    print("\nSummary\n")

    print(summary)