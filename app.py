# app.py
from flask import Flask, request, jsonify
from model.predict import predict_risk
from model.train import train_model
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        result = predict_risk(data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/train', methods=['POST'])
def train():
    try:
        data_path = 'data/sample_data.csv'
        model, scaler = train_model(data_path)
        return jsonify({'message': 'Model trained successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)