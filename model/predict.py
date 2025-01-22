import joblib
import numpy as np
from datetime import datetime

class HealthRiskAnalyzer:
    def __init__(self):
        """Initialize health parameters thresholds"""
        self.bp_thresholds = {
            'normal': {'systolic': (90, 120), 'diastolic': (60, 80)},
            'elevated': {'systolic': (120, 130), 'diastolic': (80, 85)},
            'high': {'systolic': (130, 180), 'diastolic': (85, 120)},
            'crisis': {'systolic': (180, 300), 'diastolic': (120, 200)}
        }
        
        self.bs_thresholds = {
            'normal': (3.9, 7.0),
            'pre_diabetic': (7.0, 11.0),
            'diabetic': (11.0, 25.0)
        }
        
        self.heart_rate_thresholds = {
            'low': (0, 60),
            'normal': (60, 100),
            'elevated': (100, 150),
            'high': (150, 300)
        }
        
        self.temp_thresholds = {
            'hypothermia': (0, 35),
            'normal': (35, 37.5),
            'fever': (37.5, 38.5),
            'high_fever': (38.5, 45)
        }

def load_models():
    """Load the trained model and scaler"""
    model = joblib.load('model/health_risk_model.joblib')
    scaler = joblib.load('model/health_risk_scaler.joblib')
    return model, scaler

def predict_risk(data):
    """Predict health risk level with enhanced analysis"""
    model, scaler = load_models()
    analyzer = HealthRiskAnalyzer()
    
    # Prepare input data
    features = ['Age', 'SystolicBP', 'DiastolicBP', 'BS', 'BodyTemp', 'HeartRate']
    input_data = np.array([[data.get(f, 0) for f in features]])
    
    # Scale input
    input_scaled = scaler.transform(input_data)
    
    # Make prediction
    risk_level = model.predict(input_scaled)[0]
    probabilities = model.predict_proba(input_scaled)[0]
    confidence = float(max(probabilities))
    
    # Get detailed analysis and recommendations
    analysis = analyze_vitals(data, analyzer)
    recommendations = get_recommendations(data, risk_level, analysis)
    
    return {
        'risk_level': risk_level,
        'confidence': confidence,
        'vital_signs_analysis': analysis,
        'recommendations': recommendations,
        'timestamp': datetime.now().isoformat()
    }

def analyze_vitals(data, analyzer):
    """Perform detailed analysis of vital signs"""
    analysis = {}
    
    # Blood Pressure Analysis
    systolic = data.get('SystolicBP', 0)
    diastolic = data.get('DiastolicBP', 0)
    
    bp_status = 'normal'
    for level, ranges in analyzer.bp_thresholds.items():
        if (ranges['systolic'][0] <= systolic <= ranges['systolic'][1] and 
            ranges['diastolic'][0] <= diastolic <= ranges['diastolic'][1]):
            bp_status = level
    
    analysis['blood_pressure'] = {
        'status': bp_status,
        'value': f"{systolic}/{diastolic}",
        'details': get_bp_details(bp_status)
    }
    
    # Blood Sugar Analysis
    bs = data.get('BS', 0)
    bs_status = 'normal'
    for level, (min_val, max_val) in analyzer.bs_thresholds.items():
        if min_val <= bs <= max_val:
            bs_status = level
    
    analysis['blood_sugar'] = {
        'status': bs_status,
        'value': bs,
        'details': get_bs_details(bs_status)
    }
    
    # Heart Rate Analysis
    hr = data.get('HeartRate', 0)
    hr_status = 'normal'
    for level, (min_val, max_val) in analyzer.heart_rate_thresholds.items():
        if min_val <= hr <= max_val:
            hr_status = level
    
    analysis['heart_rate'] = {
        'status': hr_status,
        'value': hr,
        'details': get_hr_details(hr_status)
    }
    
    # Temperature Analysis
    temp = data.get('BodyTemp', 0)
    temp_status = 'normal'
    for level, (min_val, max_val) in analyzer.temp_thresholds.items():
        if min_val <= temp <= max_val:
            temp_status = level
    
    analysis['temperature'] = {
        'status': temp_status,
        'value': temp,
        'details': get_temp_details(temp_status)
    }
    
    return analysis

def get_bp_details(status):
    """Get detailed blood pressure information"""
    details = {
        'normal': "Blood pressure is within healthy range.",
        'elevated': "Blood pressure is slightly elevated, indicating pre-hypertension.",
        'high': "Blood pressure is high, indicating hypertension.",
        'crisis': "Blood pressure is at crisis levels, requiring immediate medical attention."
    }
    return details.get(status, "Blood pressure status unclear.")

def get_bs_details(status):
    """Get detailed blood sugar information"""
    details = {
        'normal': "Blood sugar levels are within normal range.",
        'pre_diabetic': "Blood sugar levels indicate pre-diabetes.",
        'diabetic': "Blood sugar levels indicate diabetic range."
    }
    return details.get(status, "Blood sugar status unclear.")

def get_hr_details(status):
    """Get detailed heart rate information"""
    details = {
        'low': "Heart rate is lower than normal (bradycardia).",
        'normal': "Heart rate is within normal range.",
        'elevated': "Heart rate is elevated (mild tachycardia).",
        'high': "Heart rate is significantly elevated (tachycardia)."
    }
    return details.get(status, "Heart rate status unclear.")

def get_temp_details(status):
    """Get detailed temperature information"""
    details = {
        'hypothermia': "Body temperature is dangerously low.",
        'normal': "Body temperature is within normal range.",
        'fever': "Presence of fever indicates possible infection.",
        'high_fever': "High fever requires immediate medical attention."
    }
    return details.get(status, "Temperature status unclear.")

def get_recommendations(data, risk_level, analysis):
    """Generate comprehensive health recommendations"""
    recommendations = {
        'immediate_actions': [],
        'lifestyle_changes': [],
        'monitoring_suggestions': [],
        'follow_up_care': []
    }
    
    # Immediate Actions
    if risk_level == 'high':
        if analysis['blood_pressure']['status'] in ['high', 'crisis']:
            recommendations['immediate_actions'].extend([
                "Seek emergency medical attention for high blood pressure",
                "Take prescribed blood pressure medication if available",
                "Sit quietly and try to remain calm"
            ])
        
        if analysis['blood_sugar']['status'] == 'diabetic':
            recommendations['immediate_actions'].extend([
                "Check ketone levels if you have diabetes",
                "Take insulin or diabetes medication as prescribed",
                "Contact your healthcare provider immediately"
            ])
        
        if analysis['temperature']['status'] == 'high_fever':
            recommendations['immediate_actions'].extend([
                "Take appropriate fever-reducing medication",
                "Stay hydrated and monitor temperature regularly",
                "Seek immediate medical care if temperature continues to rise"
            ])
    
    # Lifestyle Changes
    if analysis['blood_pressure']['status'] in ['elevated', 'high']:
        recommendations['lifestyle_changes'].extend([
            "Reduce sodium intake in your diet",
            "Engage in regular physical activity",
            "Practice stress management techniques",
            "Maintain a healthy weight"
        ])
    
    if analysis['blood_sugar']['status'] in ['pre_diabetic', 'diabetic']:
        recommendations['lifestyle_changes'].extend([
            "Follow a balanced, low-glycemic diet",
            "Exercise regularly for blood sugar control",
            "Monitor carbohydrate intake",
            "Get adequate sleep"
        ])
    
    # Monitoring Suggestions
    if risk_level in ['high', 'mid']:
        recommendations['monitoring_suggestions'].extend([
            "Monitor blood pressure daily",
            "Keep a log of blood sugar readings",
            "Track heart rate during rest and activity",
            "Record any new or changing symptoms"
        ])
    
    # Follow-up Care
    if risk_level == 'high':
        recommendations['follow_up_care'].extend([
            "Schedule an immediate appointment with your healthcare provider",
            "Bring your vital signs log to your appointment",
            "Discuss medication adjustments if needed"
        ])
    elif risk_level == 'mid':
        recommendations['follow_up_care'].extend([
            "Schedule a follow-up appointment within the next week",
            "Prepare questions about lifestyle modifications",
            "Consider a medication review"
        ])
    else:
        recommendations['follow_up_care'].extend([
            "Continue regular check-ups",
            "Maintain preventive health screenings",
            "Update emergency contact information"
        ])
    
    return recommendations