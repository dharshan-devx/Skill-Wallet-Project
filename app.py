from flask import Flask, render_template, request
import numpy as np
import pickle

app = Flask(__name__)

# Load the trained model and scaler
try:
    model = pickle.load(open('model.pkl', 'rb'))
    scaler = pickle.load(open('scaler.pkl', 'rb'))
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
                    # default to 0 if not provided
                    input_features.append(0.0)
                else:
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
                prediction = -1 # Error state
                
            # Determine status
            if prediction == 1:
                status = "Credit Card Approved"
            else:
                status = "Credit Card Rejected"
                
            return render_template('result.html', prediction=prediction, status=status)
            
        except Exception as e:
            return render_template('result.html', prediction=-1, status=f"Error occurred: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
