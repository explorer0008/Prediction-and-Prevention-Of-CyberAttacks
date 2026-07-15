# CyberShield AI - Prediction and Prevention of Cyber Attacks

An end-to-end web application that detects malicious network activity using Machine Learning, automatically generates incident reports, and encrypts those reports using AES-256 to protect sensitive security information.

The project demonstrates the complete cybersecurity workflow—from data preprocessing and threat detection to secure incident reporting—through an interactive Flask-based web application.

---

## Features

- Machine Learning based cyber attack detection
- Network traffic preprocessing and feature engineering
- Multiple model training and evaluation
- Automatic best-model selection
- Interactive web interface using Flask
- Secure admin login interface
- CSV dataset upload
- Real-time attack prediction
- Threat severity analysis
- Automatic incident report generation
- AES-256 encryption of generated reports
- Confusion matrix and evaluation metrics generation

---

## Project Architecture

```
                Dataset
                   │
                   ▼
         Data Preprocessing
                   │
                   ▼
          Feature Engineering
                   │
                   ▼
      Machine Learning Model
                   │
                   ▼
          Threat Prediction
                   │
                   ▼
      Incident Report Generator
                   │
                   ▼
        AES-256 Encryption
                   │
                   ▼
      Interactive Dashboard
```

---

## Tech Stack

### Backend

- Python
- Flask
- Flask-CORS

### Machine Learning

- Scikit-Learn
- XGBoost
- LightGBM
- Pandas
- NumPy
- Joblib

### Frontend

- HTML5
- CSS3
- JavaScript

### Security

- AES-256 Encryption
- PyCryptodome

---

## Folder Structure

```
Prediction-and-Prevention-Of-CyberAttacks
│
├── datasets/
│   └── cyber_attacks.csv
│
├── ml/
│   ├── preprocess.py
│   ├── train.py
│   ├── evaluate.py
│   └── predict.py
│
├── static/
│   ├── style.css
│   └── app.js
│
├── templates/
│   ├── front.html
│   ├── index.html
│   └── dashboard.html
│
├── server.py
├── requirements.txt
└── README.md
```

---

## Machine Learning Pipeline

### 1. Data Preprocessing

- Missing value handling
- Duplicate removal
- Categorical feature encoding
- Feature scaling

### 2. Model Training

The following algorithms are trained:

- Random Forest
- XGBoost
- LightGBM

The best-performing model is automatically selected and saved.

---

## Model Performance

| Metric | Value |
|---------|--------|
| Accuracy | 88.52% |
| Precision | 99.69% |
| Recall | 74.56% |
| F1 Score | 85.31% |

---

## Application Workflow

1. User opens the application.
2. Admin signs in.
3. User uploads a CSV containing network traffic.
4. The backend preprocesses the dataset.
5. The trained model predicts malicious activity.
6. Threat statistics are generated.
7. An incident report is created.
8. The report is encrypted using AES-256.
9. Results are displayed on the dashboard.

---

## Installation

Clone the repository

```bash
git clone https://github.com/explorer0008/Prediction-and-Prevention-Of-CyberAttacks.git
```

Move into the project directory

```bash
cd Prediction-and-Prevention-Of-CyberAttacks
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Project

### Train the model

```bash
python ml/preprocess.py
python ml/train.py
python ml/evaluate.py
```

### Start the server

```bash
python server.py
```

Open your browser

```
http://127.0.0.1:5000
```

---

## Sample Dataset

The project uses a structured network intrusion dataset containing features such as:

- Session ID
- Protocol Type
- Packet Size
- Session Duration
- Failed Login Attempts
- Browser Type
- Encryption Used
- IP Reputation Score
- Login Attempts
- Unusual Access Time

Target Variable:

```
attack_detected
```

---

## Security Features

- AES-256 encrypted incident reports
- Unique incident identifiers
- Secure report storage
- Threat severity classification
- Prediction summaries
- Report metadata generation

---

## Future Improvements

- Deep Learning based intrusion detection
- Multi-class attack classification
- JWT authentication
- Database integration
- Real-time packet capture
- Live monitoring dashboard
- Docker deployment
- Cloud deployment
- Email alerts
- SIEM integration

---

## Learning Outcomes

This project demonstrates practical knowledge of:

- Machine Learning
- Data Preprocessing
- Feature Engineering
- Cybersecurity Analytics
- Flask Backend Development
- REST API Development
- Encryption Techniques
- Full Stack Development
- Software Architecture
- Model Evaluation

<img width="646" height="397" alt="image" src="https://github.com/user-attachments/assets/c2a1af8b-b411-4d68-80a6-b4aac50b5264" />
<img width="633" height="397" alt="image" src="https://github.com/user-attachments/assets/4cdda12e-3693-4d07-8cd0-479768c7bc9e" />
<img width="635" height="176" alt="image" src="https://github.com/user-attachments/assets/f626a32b-5c2c-4880-95f4-51b858a7a5e6" />

<img width="632" height="387" alt="image" src="https://github.com/user-attachments/assets/80a64c67-1b4f-4209-b83d-7c91d406c0ba" />
