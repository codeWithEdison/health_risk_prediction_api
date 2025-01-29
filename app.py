import os
from flask import Flask
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix

# Handle dotenv import
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Import after environment is set up
from model.predict import predict_risk
from model.train import train_model

# Create Flask app
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

# Create Flask-RESTX API with documentation
api = Api(app, 
          version='1.0', 
          title='Health Risk Prediction API',
          description='An API for predicting health risks based on vital signs',
          doc='/swagger-ui'  # This will serve Swagger UI at the /swagger-ui endpoint
)

# Create namespaces
health_ns = api.namespace('health', description='Health check operations')
prediction_ns = api.namespace('prediction', description='Health risk prediction')
training_ns = api.namespace('training', description='Model training operations')

# Define input and output models for Swagger documentation
vital_signs_model = api.model('VitalSigns', {
    'Age': fields.Integer(required=True, description='Patient age', example=35),
    'SystolicBP': fields.Integer(required=True, description='Systolic Blood Pressure', example=120),
    'DiastolicBP': fields.Integer(required=True, description='Diastolic Blood Pressure', example=80),
    'BS': fields.Float(required=True, description='Blood Sugar Level', example=5.5),
    'BodyTemp': fields.Float(required=True, description='Body Temperature', example=36.6),
    'HeartRate': fields.Integer(required=True, description='Heart Rate', example=72)
})

prediction_response_model = api.model('PredictionResponse', {
    'risk_level': fields.String(description='Predicted risk level', example='low'),
    'confidence': fields.Float(description='Prediction confidence', example=0.85),
    'vital_signs_analysis': fields.Raw(description='Detailed analysis of vital signs'),
    'recommendations': fields.Raw(description='Health recommendations'),
    'timestamp': fields.String(description='Prediction timestamp')
})

# Health Check Resource
@health_ns.route('/')
class HealthCheck(Resource):
    def get(self):
        """Perform a health check on the API"""
        return {'status': 'healthy'}

# Prediction Resource
@prediction_ns.route('/')
class HealthPrediction(Resource):
    @prediction_ns.expect(vital_signs_model)
    @prediction_ns.marshal_with(prediction_response_model)
    def post(self):
        """Predict health risk based on vital signs"""
        try:
            data = api.payload
            result = predict_risk(data)
            return result, 200
        except Exception as e:
            api.abort(400, str(e))

# Training Resource
@training_ns.route('/')
class ModelTraining(Resource):
    def post(self):
        """Train the health risk prediction model"""
        try:
            data_path = os.path.join(os.path.dirname(__file__), 'data', 'sample_data.csv')
            model, scaler = train_model(data_path)
            return {'message': 'Model trained successfully'}, 200
        except Exception as e:
            api.abort(400, str(e))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)