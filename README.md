# 🏥 Health Risk Prediction API

![Python Version](https://img.shields.io/badge/Python-3.10-blue.svg)
![Flask Version](https://img.shields.io/badge/Flask-3.1.0-green.svg)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.6.0-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

A sophisticated machine learning-powered API that predicts health risks and provides personalized medical recommendations based on vital signs and health metrics. Built with Flask and Scikit-learn, this API offers real-time health risk assessment and clinical decision support.

## 🌟 Key Features

- **Instant Risk Assessment** - Real-time evaluation of patient health status
- **Comprehensive Analysis** - Multi-parameter vital signs monitoring
- **Smart Recommendations** - AI-powered health advice
- **Clinical Support** - Evidence-based risk categorization
- **Easy Integration** - RESTful API endpoints

## 🎯 Risk Categories & Monitoring

### Vital Signs Monitored
- Blood Pressure (Systolic/Diastolic)
- Blood Sugar Levels
- Body Temperature
- Heart Rate
- Age Factor

### Risk Levels
- **High Risk** - Immediate medical attention required
- **Mid Risk** - Close monitoring needed
- **Low Risk** - Regular health maintenance

## 🚀 Getting Started

### Prerequisites
```bash
python 3.10 or higher
pip (Python package manager)
git
```

### Installation

1. Clone the repository:
```bash
git clone https://github.com/codeWithEdison/health_risk_prediction_api.git
cd health_risk_prediction_api
```

2. Set up virtual environment:
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
source venv/bin/activate      # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the API:
```bash
python app.py
```

## 📡 API Endpoints

### Check API Health
```http
GET /health
```

### Train the Model
```http
POST /api/train
```

### Get Health Risk Prediction
```http
POST /api/predict
```

#### Example Request
```json
{
    "Age": 45,
    "SystolicBP": 145,
    "DiastolicBP": 95,
    "BS": 12.5,
    "BodyTemp": 38.2,
    "HeartRate": 98
}
```

#### Example Response
```json
{
    "risk_level": "high",
    "confidence": 0.92,
    "vital_signs_analysis": {
        "blood_pressure": {
            "status": "high",
            "value": "145/95",
            "details": "Blood pressure is high, indicating hypertension."
        }
    },
    "recommendations": {
        "immediate_actions": [
            "Seek emergency medical attention for high blood pressure"
        ],
        "lifestyle_changes": [
            "Reduce sodium intake",
            "Regular exercise"
        ],
        "monitoring_suggestions": [
            "Daily blood pressure monitoring"
        ]
    }
}
```

## 📊 Health Metrics Thresholds

### Blood Pressure (mmHg)
- **Normal**: 90-120/60-80
- **Elevated**: 120-130/80-85
- **High**: 130-180/85-120
- **Crisis**: >180/>120

### Blood Sugar (mmol/L)
- **Normal**: 3.9-7.0
- **Pre-diabetic**: 7.0-11.0
- **Diabetic**: >11.0

### Body Temperature (°C)
- **Normal**: 35-37.5
- **Fever**: 37.5-38.5
- **High Fever**: >38.5

### Heart Rate (bpm)
- **Normal**: 60-100
- **Elevated**: 100-150
- **High**: >150

## 🛠️ Technology Stack

- **Flask** - Web framework
- **Scikit-learn** - Machine learning
- **NumPy** - Numerical computations
- **Pandas** - Data manipulation
- **Gunicorn** - WSGI HTTP Server

## 🚀 Deployment Guide

This API is ready for deployment on Render:

1. Fork this repository
2. Create new Web Service on Render
3. Connect to your GitHub repository
4. Configure build settings:
   ```
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app
   ```
5. Set environment variables:
   - `PYTHON_VERSION`: 3.10.0
   - `PORT`: 10000

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit changes (`git commit -m 'Add YourFeature'`)
4. Push to branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

## 📧 Contact

Edison - [GitHub](https://github.com/codeWithEdison)

Project Link: [https://github.com/codeWithEdison/health_risk_prediction_api](https://github.com/codeWithEdison/health_risk_prediction_api)

## 🙏 Acknowledgments

- World Health Organization (WHO) guidelines
- American Heart Association recommendations
- International Diabetes Federation standards

---
Built with ❤️ by [codeWithEdison](https://github.com/codeWithEdison)