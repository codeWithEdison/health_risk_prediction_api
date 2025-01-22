import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib

def train_model(data_path):
    """Train the health risk prediction model"""
    # Load and prepare data
    df = pd.read_csv(data_path)
    df['RiskLevel'] = df['RiskLevel'].str.lower().str.replace(' risk', '')
    
    # Prepare features and target
    features = ['Age', 'SystolicBP', 'DiastolicBP', 'BS', 'BodyTemp', 'HeartRate']
    X = df[features]
    y = df['RiskLevel']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    # Save model and scaler
    joblib.dump(model, 'model/health_risk_model.joblib')
    joblib.dump(scaler, 'model/health_risk_scaler.joblib')
    
    return model, scaler