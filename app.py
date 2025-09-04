from flask import Flask, request, jsonify
from flask_cors import CORS
from model import predict_hazard
import os

app = Flask(__name__)

# Configure CORS to allow requests from your frontend
CORS(app, origins=[
    "https://simhastha-safety.netlify.app",
    # http://127.0.0.1:5500/
    "http://localhost:3000",  # for local development
    "http://127.0.0.1:5500"   # alternative local address
])

@app.route("/")
def home():
    return jsonify({
        "message": "Hazard Alert System API is running",
        "status": "active",
        "version": "1.0"
    })

@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/predict", methods=["POST", "OPTIONS"])
def predict():
    # Handle preflight requests
    if request.method == "OPTIONS":
        return "", 200
    
    try:
        data = request.get_json()
        
        # Validate input data
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        crowd_density = float(data.get("crowd_density", 0))
        temperature = float(data.get("temperature", 25))
        movement_speed = float(data.get("movement_speed", 1.0))
        
        # Validate ranges (adjust based on your model requirements)
        if crowd_density < 0 or crowd_density > 100:
            return jsonify({"error": "Crowd density must be between 0 and 100"}), 400
        
        if temperature < -50 or temperature > 60:
            return jsonify({"error": "Temperature must be between -50°C and 60°C"}), 400
        
        if movement_speed < 0 or movement_speed > 10:
            return jsonify({"error": "Movement speed must be between 0 and 10"}), 400
        
        result = predict_hazard(crowd_density, temperature, movement_speed)
        
        return jsonify({
            "success": True,
            "prediction": result,
            "input_data": {
                "crowd_density": crowd_density,
                "temperature": temperature,
                "movement_speed": movement_speed
            }
        })
        
    except ValueError as ve:
        return jsonify({"error": f"Invalid input data: {str(ve)}"}), 400
    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    # Use environment variables for production deployment
    port = int(os.environ.get("PORT", 5001))
    debug_mode = os.environ.get("FLASK_ENV") == "development"
    
    app.run(
        host="0.0.0.0",  # Important for deployment
        port=port,
        debug=debug_mode
    )