print("EVALUATE.PY STARTED")
import os
import joblib
import warnings
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

from preprocess import DataPreprocessor

warnings.filterwarnings("ignore")


class ModelEvaluator:

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

        self.model = joblib.load(
            "models/model.pkl"
        )

        os.makedirs(
            "reports",
            exist_ok=True
        )

    def evaluate(self):

        predictions = self.model.predict(
            self.X_test
        )

        metrics = {

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

        print("\nEvaluation Metrics\n")

        for key, value in metrics.items():

            print(f"{key.capitalize()} : {value:.4f}")

        joblib.dump(
            metrics,
            "models/evaluation_metrics.pkl"
        )

        report = classification_report(
            self.y_test,
            predictions
        )

        with open(
            "reports/classification_report.txt",
            "w"
        ) as file:

            file.write(report)

        matrix = confusion_matrix(
            self.y_test,
            predictions
        )

        display = ConfusionMatrixDisplay(
            confusion_matrix=matrix
        )

        fig, ax = plt.subplots(figsize=(6,6))

        display.plot(
            ax=ax,
            cmap="Blues",
            colorbar=False
        )

        plt.title("Confusion Matrix")

        plt.tight_layout()

        plt.savefig(
            "reports/confusion_matrix.png"
        )

        plt.close()

        print("\nEvaluation Completed Successfully")


if __name__ == "__main__":

    print("Starting Evaluation...")

    evaluator = ModelEvaluator()

    evaluator.evaluate()

    print("Evaluation Completed.")