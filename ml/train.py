import os
import joblib
import warnings

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

from preprocess import DataPreprocessor

warnings.filterwarnings("ignore")


class ModelTrainer:

    def __init__(self):

        processor = DataPreprocessor(
            "datasets/cyber_attacks.csv"
        )

        (
            self.X_train,
            self.X_test,
            self.y_train,
            self.y_test
        ) = processor.preprocess()

        self.models = {

            "Random Forest": RandomForestClassifier(
                n_estimators=300,
                random_state=42,
                n_jobs=-1
            ),

            "XGBoost": XGBClassifier(
                random_state=42,
                eval_metric="logloss",
                use_label_encoder=False
            ),

            "LightGBM": LGBMClassifier(
                random_state=42
            )

        }

        self.best_model = None
        self.best_name = None
        self.best_accuracy = -1
        self.metrics = {}

    def evaluate(self, predictions):

        return {

            "accuracy": accuracy_score(
                self.y_test,
                predictions
            ),

            "precision": precision_score(
                self.y_test,
                predictions
            ),

            "recall": recall_score(
                self.y_test,
                predictions
            ),

            "f1": f1_score(
                self.y_test,
                predictions
            )

        }

    def train(self):

        print("\nTraining Models...\n")

        for name, model in self.models.items():

            print(f"Training {name}")

            model.fit(
                self.X_train,
                self.y_train
            )

            predictions = model.predict(
                self.X_test
            )

            metric = self.evaluate(
                predictions
            )

            self.metrics[name] = metric

            print(metric)

            if metric["accuracy"] > self.best_accuracy:

                self.best_accuracy = metric["accuracy"]

                self.best_model = model

                self.best_name = name

    def save(self):

        os.makedirs(
            "models",
            exist_ok=True
        )

        joblib.dump(
            self.best_model,
            "models/model.pkl"
        )

        joblib.dump(
            self.metrics[self.best_name],
            "models/model_metrics.pkl"
        )

        print("\nBest Model :", self.best_name)
        print("Accuracy :", self.best_accuracy)

    def run(self):

        self.train()

        self.save()


if __name__ == "__main__":

    trainer = ModelTrainer()

    trainer.run()