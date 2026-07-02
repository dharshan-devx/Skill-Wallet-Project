import os
from flask import Flask, render_template, request
import numpy as np
import pickle
from waitress import serve

app = Flask(__name__)

# Absolute paths for robust loading
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'model.pkl')
SCALER_PATH = os.path.join(BASE_DIR, 'scaler.pkl')

# Load the trained model and scaler
try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    with open(SCALER_PATH, 'rb') as f:
        scaler = pickle.load(f)
except Exception as e:
    print(f"Error loading model/scaler: {e}")
    model = None
    scaler = None

# Feature columns exactly as in the notebook
FEATURES = ['Time'] + [f'V{i}' for i in range(1, 29)] + ['Amount']

@app.route('/')
def home():
    """Render the home page."""
    return render_template('home.html')

@app.route('/predict')
def predict():
    """Render the prediction form."""
    return render_template('index.html', features=FEATURES)

@app.route('/result', methods=['POST'])
def result():
    """Process form data, scale, predict, and render result."""
    if request.method == 'POST':
        try:
            # Extract features from form exactly in the order of FEATURES
            input_features = []
            for col in FEATURES:
                val = request.form.get(col)
                if val is None or val.strip() == '':
                    # Strict validation: prevent defaulting to 0.0
                    raise ValueError(f"Missing required input for feature: {col}")
                input_features.append(float(val))
            
            # Convert to numpy array and reshape for prediction
            features_array = np.array(input_features).reshape(1, -1)
            
            # Scale numerical values as in notebook
            if scaler:
                features_scaled = scaler.transform(features_array)
            else:
                features_scaled = features_array
                
            # Predict
            if model:
                prediction = model.predict(features_scaled)[0]
            else:
                raise RuntimeError("Model is not loaded properly.")
                
            # Determine status
            if prediction == 1:
                status = "Credit Card Approved"
            else:
                status = "Credit Card Rejected"
                
            return render_template('result.html', prediction=prediction, status=status)
            
        except ValueError as ve:
            # Handle bad input from the user specifically
            return render_template('result.html', prediction=-1, status=f"Input Error: {str(ve)}")
        except Exception as e:
            # Handle other runtime errors
            return render_template('result.html', prediction=-1, status=f"Error occurred: {str(e)}")

if __name__ == '__main__':
    print("Starting production Waitress server on http://0.0.0.0:5000")
    serve(app, host='0.0.0.0', port=5000)
