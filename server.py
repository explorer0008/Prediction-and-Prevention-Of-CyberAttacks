import os
import json
import uuid
import base64
import logging
import traceback
from datetime import datetime

from flask import (
    Flask,
    jsonify,
    request,
    render_template
)

from flask_cors import CORS

from werkzeug.utils import secure_filename

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

import joblib

from ml.predict import Predictor


app = Flask(__name__)

CORS(app)


UPLOAD_FOLDER = "uploads"
REPORT_FOLDER = "reports"
MODEL_FOLDER = "models"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)
os.makedirs(MODEL_FOLDER, exist_ok=True)


logging.basicConfig(

    filename="server.log",

    level=logging.INFO,

    format="%(asctime)s | %(levelname)s | %(message)s"

)


predictor = Predictor()


try:

    MODEL_METRICS = joblib.load(

        os.path.join(

            MODEL_FOLDER,

            "model_metrics.pkl"

        )

    )

except Exception:

    MODEL_METRICS = {

        "accuracy":0,

        "precision":0,

        "recall":0,

        "f1":0

    }


AES_KEY = get_random_bytes(32)
@app.route("/")
def home():

    return render_template(

        "front.html"

    )
@app.route("/login")
def login():

    return render_template("index.html")
@app.route("/home")
def home_page():
    return render_template("front.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")
@app.route("/dashboard.html")
def dashboard_html():

    return render_template("dashboard.html")


@app.route("/index.html")
def index_html():

    return render_template("index.html")


@app.route("/front.html")
def front_html():

    return render_template("front.html")


@app.route("/health")
def health():

    return jsonify({

        "status":"Healthy",

        "model_loaded":True,

        "prediction_engine":"Ready"

    })


def generate_incident_report(summary):

    return {

        "incident_id":str(uuid.uuid4()),

        "timestamp":datetime.now().strftime(

            "%Y-%m-%d %H:%M:%S"

        ),

        "severity":summary["severity"],

        "threat_score":summary["threat_score"],

        "attack_packets":summary["attack_packets"],

        "benign_packets":summary["benign_packets"],

        "total_packets":summary["total_packets"],

        "recommendation":(

            "Immediately isolate the affected host "

            "and inspect firewall and IDS logs."

            if summary["attack_packets"] > 0

            else

            "No suspicious activity detected."

        )

    }


def encrypt_report(report):

    report_json = json.dumps(

        report,

        indent=4

    )

    cipher = AES.new(

        AES_KEY,

        AES.MODE_CBC

    )

    encrypted = cipher.encrypt(

        pad(

            report_json.encode(),

            AES.block_size

        )

    )

    return (

        cipher.iv +

        encrypted

    )


def decrypt_report_data(data):

    iv = data[:16]

    ciphertext = data[16:]

    cipher = AES.new(

        AES_KEY,

        AES.MODE_CBC,

        iv

    )

    decrypted = unpad(

        cipher.decrypt(ciphertext),

        AES.block_size

    )

    return json.loads(

        decrypted.decode()

    )
@app.route("/predict", methods=["POST"])
def predict():

    try:

        if "dataset" not in request.files:

            return jsonify({

                "error":"Dataset not found."

            }),400

        file = request.files["dataset"]

        if file.filename == "":

            return jsonify({

                "error":"Invalid filename."

            }),400

        filename = secure_filename(

            file.filename

        )

        upload_path = os.path.join(

            UPLOAD_FOLDER,

            filename

        )

        file.save(upload_path)

        predictions, summary = predictor.run(

            upload_path

        )

        incident_report = generate_incident_report(

            summary

        )

        encrypted_report = encrypt_report(

            incident_report

        )

        encrypted_filename = (

            incident_report["incident_id"]

            + ".enc"

        )

        encrypted_path = os.path.join(

            REPORT_FOLDER,

            encrypted_filename

        )

        with open(

            encrypted_path,

            "wb"

        ) as report_file:

            report_file.write(

                encrypted_report

            )
            metadata = {

            "incident_id":

                incident_report["incident_id"],

            "timestamp":

                incident_report["timestamp"],

            "severity":

                incident_report["severity"],

            "threat_score":

                incident_report["threat_score"],

            "encrypted_file":

                encrypted_filename

        }

        metadata_path = os.path.join(

            REPORT_FOLDER,

            incident_report["incident_id"]

            + ".json"

        )

        with open(

            metadata_path,

            "w"

        ) as metadata_file:

            json.dump(

                metadata,

                metadata_file,

                indent=4

            )

        response = {

            "accuracy":

                MODEL_METRICS["accuracy"],

            "precision":

                MODEL_METRICS["precision"],

            "recall":

                MODEL_METRICS["recall"],

            "f1_score":

                MODEL_METRICS["f1"],

            "summary":

                summary,

            "incident":

                incident_report

        }

        return jsonify(

            response

        )

    except Exception as error:

        logging.error(

            traceback.format_exc()

        )

        return jsonify({

            "error":str(error)

        }),500
    @app.route("/reports", methods=["GET"])

    def reports():

     report_list = []

    for file in os.listdir(REPORT_FOLDER):

        if file.endswith(".json"):

            path = os.path.join(

                REPORT_FOLDER,

                file

            )

            with open(path, "r") as metadata:

                report_list.append(

                    json.load(metadata)

                )

    report_list.sort(

        key=lambda x: x["timestamp"],

        reverse=True

    )

    return jsonify(report_list)
@app.route("/decrypt/<incident_id>", methods=["GET"])
def decrypt(incident_id):

    try:

        encrypted_path = os.path.join(

            REPORT_FOLDER,

            incident_id + ".enc"

        )

        if not os.path.exists(

            encrypted_path

        ):

            return jsonify({

                "error":"Report not found."

            }),404

        with open(

            encrypted_path,

            "rb"

        ) as file:

            encrypted_data = file.read()

        report = decrypt_report_data(

            encrypted_data

        )

        return jsonify(report)

    except Exception as error:

        logging.error(

            traceback.format_exc()

        )

        return jsonify({

            "error":str(error)

        }),500
    @app.route("/download/<incident_id>", methods=["GET"])
    def download_metadata(incident_id):

     metadata_path = os.path.join(

        REPORT_FOLDER,

        incident_id + ".json"

    )

    if not os.path.exists(

        metadata_path

    ):

        return jsonify({

            "error":"Metadata not found."

        }),404

    with open(

        metadata_path,

        "r"

    ) as file:

        metadata = json.load(file)

    return jsonify(metadata)
@app.errorhandler(404)
def not_found(error):

    return jsonify({

        "error":"Route not found."

    }),404


@app.errorhandler(500)
def internal_server_error(error):

    return jsonify({

        "error":"Internal server error."

    }),500


if __name__ == "__main__":

    print()

    print("====================================")

    print("   CyberShield AI Backend Started   ")

    print("====================================")

    print()

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )
