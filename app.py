import os
import ssl
import pymysql
import sqlalchemy
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource, fields
from sqlalchemy import desc, text
from dotenv import load_dotenv
from datetime import date, datetime

# Load environment variables
load_dotenv()

# Install pymysql as MySQLdb
pymysql.install_as_MySQLdb()

# Import prediction model
from model.predict import predict_risk

# Create Flask app
app = Flask(__name__)



# Database Configuration
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
db_name = os.getenv('DB_NAME', 'patient_management')
db_ca_cert = os.getenv('DB_CA_CERT_PATH')

# Construct connection string
connection_string = (
    f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    f"?ssl_ca={db_ca_cert}"
    f"&ssl_verify_cert=false"
)

# App configuration
app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'connect_args': {
        'ssl': {
            'ca': db_ca_cert,
            'check_hostname': False,
            'verify_mode': ssl.CERT_NONE
        }
    }
}

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Create Flask-RESTX API with Swagger documentation
api = Api(app, 
          version='1.0', 
          title='Patient Risk Prediction API',
          description='API for retrieving and predicting patient health risks',
          doc='/swagger')

# Define SQLAlchemy models to match the database schema
class Patient(db.Model):
    __tablename__ = 'patient'
    patient_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)

class MedicalRecord(db.Model):
    __tablename__ = 'medical_record'
    record_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'), nullable=False)
    visit_date = db.Column(db.DateTime, nullable=False)
    temperature = db.Column(db.Float)
    blood_pressure_sys = db.Column(db.Integer)
    blood_pressure_dia = db.Column(db.Integer)
    heart_rate = db.Column(db.Integer)
    blood_sugar = db.Column(db.Float)

class HealthRiskPrediction(db.Model):
    __tablename__ = 'health_risk_prediction'
    prediction_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'), nullable=False)
    record_id = db.Column(db.Integer, db.ForeignKey('medical_record.record_id'), nullable=False)
    risk_level = db.Column(db.Enum('low', 'medium', 'high'), nullable=False)
    prediction_details = db.Column(db.Text, nullable=False)
    recommendations = db.Column(db.Text, nullable=False)
    predicted_at = db.Column(db.DateTime, server_default=db.func.now())

# Namespaces
prediction_ns = api.namespace('prediction', description='Health Risk Prediction Operations')

# Swagger Models for Request and Response
patient_prediction_model = api.model('PatientPrediction', {
    'patient_id': fields.Integer(required=True, description='Patient ID to predict risk for', example=1)
})

prediction_response_model = api.model('PredictionResponse', {
    'patient_id': fields.Integer(description='Patient ID'),
    'patient_name': fields.String(description='Patient Full Name'),
    'patient_age': fields.Integer(description='Calculated Patient Age'),
    'risk_prediction': fields.Raw(description='Detailed Risk Prediction'),
    'medical_record': fields.Raw(description='Latest Medical Record Details')
})

# Prediction Resource with Swagger Documentation
# In your prediction endpoint
@prediction_ns.route('/')
class PatientRiskPrediction(Resource):
    @prediction_ns.expect(patient_prediction_model)
    @prediction_ns.marshal_with(prediction_response_model)
    def post(self):
        """
        Predict health risk for a specific patient
        """
        try:
            # Get patient ID from request
            patient_id = request.json.get('patient_id')
            
            # Validate patient exists
            patient = Patient.query.get_or_404(patient_id, description="Patient not found")
            
            # Calculate patient age
            today = date.today()
            age = today.year - patient.birth_date.year - (
                (today.month, today.day) < (patient.birth_date.month, patient.birth_date.day)
            )
            
            # Find the latest medical record
            latest_record = (MedicalRecord.query
                             .filter_by(patient_id=patient_id)
                             .order_by(desc(MedicalRecord.visit_date))
                             .first())
            
            if not latest_record:
                api.abort(404, f"No medical records found for patient {patient_id}")
            
            # Prepare prediction input data
            prediction_input = {
                'Age': age,
                'SystolicBP': latest_record.blood_pressure_sys or 0,
                'DiastolicBP': latest_record.blood_pressure_dia or 0,
                'BS': latest_record.blood_sugar or 0,
                'BodyTemp': latest_record.temperature or 0,
                'HeartRate': latest_record.heart_rate or 0
            }
            
            # Make risk prediction
            risk_prediction = predict_risk(prediction_input)
            
            # Save prediction to database
            new_prediction = HealthRiskPrediction(
                patient_id=patient_id,
                record_id=latest_record.record_id,
                risk_level=risk_prediction['risk_level'],
                prediction_details=str(risk_prediction['vital_signs_analysis']),
                recommendations=str(risk_prediction['recommendations'])
            )
            db.session.add(new_prediction)
            db.session.commit()
            
            # Prepare response with safe serialization
            response = {
                'patient_id': patient_id,
                'patient_name': patient.full_name,
                'patient_age': age,
                'risk_prediction': risk_prediction,
                'medical_record': {
                    'visit_date': latest_record.visit_date.isoformat() if latest_record.visit_date else None,
                    'blood_pressure': f"{latest_record.blood_pressure_sys}/{latest_record.blood_pressure_dia}",
                    'blood_sugar': latest_record.blood_sugar,
                    'temperature': latest_record.temperature,
                    'heart_rate': latest_record.heart_rate
                }
            }
            
            return response, 200
        
        except Exception as e:
            db.session.rollback()
            api.abort(500, f"An error occurred: {str(e)}")
# Database Connection Test Endpoint
@api.route('/db-test')
class DatabaseConnectionTest(Resource):
    def get(self):
        """
        Test database connection
        
        Returns connection status and additional database information
        """
        try:
            # Simple connection test using SQLAlchemy core
            with db.engine.connect() as connection:
                # Basic query to test connection
                result = connection.execute(text('SELECT 1'))
                result.fetchone()
            
            return {
                'status': 'Database connection successful',
                'details': {
                    'host': db_host,
                    'port': db_port,
                    'database': db_name
                }
            }, 200
        except Exception as e:
            return {
                'status': 'Database connection failed', 
                'error': str(e),
                'connection_details': {
                    'host': db_host,
                    'port': db_port,
                    'database': db_name
                }
            }, 500

# Health Check Endpoint
@api.route('/health')
class HealthCheck(Resource):
    def get(self):
        """
        Check API health status
        
        Returns a simple status to confirm the API is running
        """
        return {'status': 'healthy'}, 200

# Debugging function to print connection details (optional)
def print_connection_debug_info():
    print("Database Connection Details:")
    print(f"Host: {db_host}")
    print(f"Port: {db_port}")
    print(f"User: {db_user}")
    print(f"Database: {db_name}")
    print(f"SSL Cert Path: {db_ca_cert}")

if __name__ == '__main__':
    # Print connection debug info
    print_connection_debug_info()
    
    # Run the application
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)