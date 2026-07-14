from flask import Flask, request, jsonify
from flask_cors import CORS
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64
import json
import uuid
import pandas as pd
import numpy as np
import joblib
import os
import time

app = Flask(__name__)

CORS(app)

UPLOAD_FOLDER = "uploads"

MODEL_FOLDER = "trained_models"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model = None

try:

    model = joblib.load(

        os.path.join(
            MODEL_FOLDER,
            "model.pkl"
        )

    )

    print("Model Loaded Successfully")

except Exception:

    print("Model not found. Running in demo mode.")
    @app.route("/")

def home():

    return jsonify({

        "application":"CyberShield AI",

        "status":"Running"

    })


@app.route("/health")

def health():

    return jsonify({

        "status":"Healthy",

        "model_loaded":model is not None

    })


@app.route("/predict", methods=["POST"])

def predict():

    if "dataset" not in request.files:

        return jsonify({

            "error":"Dataset not provided."

        }),400

    file=request.files["dataset"]

    if file.filename=="":

        return jsonify({

            "error":"Invalid file."

        }),400

    path=os.path.join(

        UPLOAD_FOLDER,

        file.filename

    )

    file.save(path)

    dataframe=pd.read_csv(path)

    start=time.time()
        try:

        if dataframe.empty:

            return jsonify({

                "error": "Uploaded dataset is empty."

            }), 400

        dataframe.drop_duplicates(inplace=True)

        dataframe.fillna(0, inplace=True)

        total_packets = len(dataframe)

        if model is None:

            predictions = np.random.choice(

                [

                    "Benign",

                    "DDoS",

                    "Port Scan",

                    "Brute Force",

                    "Botnet"

                ],

                size=total_packets,

                p=[0.70,0.08,0.08,0.07,0.07]

            )

        else:

            predictions = model.predict(dataframe)
        dataframe["Prediction"] = predictions

        attack_data = dataframe[

            dataframe["Prediction"] != "Benign"

        ]

        attack_count = len(attack_data)

        benign_count = total_packets - attack_count

        attack_distribution = (

            dataframe["Prediction"]

            .value_counts()

            .to_dict()

        )

        highest_threat = (

            max(

                attack_distribution,

                key=attack_distribution.get

            )

        )

        threat_score = round(

            (attack_count / total_packets) * 100,

            2

        )

        prediction_time = round(

            (time.time() - start) * 1000,

            2

        )
                    severity = "Low"

        if threat_score >= 70:

            severity = "Critical"

        elif threat_score >= 40:

            severity = "High"

        elif threat_score >= 15:

            severity = "Medium"

        recommendation = {

            "Benign":"No action required.",

            "DDoS":"Enable rate limiting and block suspicious IPs.",

            "Port Scan":"Inspect firewall logs and block scanner.",

            "Brute Force":"Lock targeted accounts and enable MFA.",

            "Botnet":"Isolate infected systems immediately."

        }

        incident_report = {

            "incident_id":str(uuid.uuid4()),

            "timestamp":time.strftime("%Y-%m-%d %H:%M:%S"),

            "total_packets":total_packets,

            "attack_packets":attack_count,

            "highest_threat":highest_threat,

            "severity":severity,

            "threat_score":threat_score,

            "prediction_time":prediction_time,

            "recommendation":

                recommendation.get(

                    highest_threat,

                    "Further investigation required."

                )

        }
        report_json = json.dumps(

            incident_report,

            indent=4

        )

        aes_key = get_random_bytes(32)

        cipher = AES.new(

            aes_key,

            AES.MODE_CBC

        )

        encrypted_report = cipher.encrypt(

            pad(

                report_json.encode(),

                AES.block_size

            )

        )

        encrypted_file = (

            incident_report["incident_id"]

            + ".enc"

        )

        with open(

            os.path.join(

                REPORT_FOLDER,

                encrypted_file

            ),

            "wb"

        ) as file:

            file.write(

                cipher.iv +

                encrypted_report

            )
