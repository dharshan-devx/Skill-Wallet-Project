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
    print("Model and scaler loaded successfully.")
except Exception as e:
    print(f"Error loading model/scaler: {e}")
    model = None
    scaler = None

# Encoding maps matching the training script
GENDER_MAP = {'FEMALE': 0, 'MALE': 1}
BINARY_MAP = {'NO': 0, 'YES': 1}

INCOME_TYPE_MAP = {
    'Working': 0,
    'Commercial associate': 1,
    'Pensioner': 2,
    'State servant': 3,
    'Student': 4
}

EDUCATION_MAP = {
    'Lower secondary': 0,
    'Secondary / secondary special': 1,
    'Incomplete higher': 2,
    'Higher education': 3,
    'Academic degree': 4
}

FAMILY_STATUS_MAP = {
    'Single / not married': 0,
    'Married': 1,
    'Civil marriage': 2,
    'Widow': 3,
    'Separated': 4
}

HOUSING_MAP = {
    'Rented apartment': 0,
    'House / apartment': 1,
    'Municipal apartment': 2,
    'With parents': 3,
    'Co-op apartment': 4,
    'Office apartment': 5
}

@app.route('/')
def home():
    """Render the home/prediction form."""
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    """Process form data, encode, scale, predict, and render result."""
    if request.method == 'POST':
        try:
            gender      = GENDER_MAP[request.form['gender']]
            own_car     = BINARY_MAP[request.form['own_car']]
            own_realty  = BINARY_MAP[request.form['own_realty']]
            income      = float(request.form['income'])
            income_type = INCOME_TYPE_MAP[request.form['income_type']]
            education   = EDUCATION_MAP[request.form['education']]
            family_status = FAMILY_STATUS_MAP[request.form['family_status']]
            housing     = HOUSING_MAP[request.form['housing']]
            days_birth  = float(request.form['days_birth'])
            days_employed = float(request.form['days_employed'])
            family_members = float(request.form['family_members'])
            emi_paid_off = float(request.form['emi_paid_off'])
            emi_pastdues = float(request.form['emi_pastdues'])
            num_loans   = float(request.form['num_loans'])

            features = np.array([[
                gender, own_car, own_realty, income, income_type, education,
                family_status, housing, days_birth, days_employed,
                family_members, emi_paid_off, emi_pastdues, num_loans
            ]])

            if scaler:
                features = scaler.transform(features)

            if model:
                prediction = model.predict(features)[0]
                probability = model.predict_proba(features)[0]
                confidence = round(float(max(probability)) * 100, 1)
            else:
                raise RuntimeError("Model is not loaded properly.")

            if prediction == 1:
                status = "Credit Card Approved"
            else:
                status = "Credit Card Rejected"

            return render_template('result.html',
                                   prediction=int(prediction),
                                   status=status,
                                   confidence=confidence)

        except ValueError as ve:
            return render_template('result.html', prediction=-1,
                                   status=f"Input Error: {str(ve)}", confidence=0)
        except Exception as e:
            return render_template('result.html', prediction=-1,
                                   status=f"Error: {str(e)}", confidence=0)

if __name__ == '__main__':
    print("Starting production Waitress server on http://0.0.0.0:5000")
    serve(app, host='0.0.0.0', port=5000)
