# Credit Card Approval Prediction

## Project Overview
This project is a complete end-to-end Machine Learning web application for predicting Credit Card Approvals. 
It takes an uploaded Jupyter Notebook's machine learning logic and transforms it into a production-ready Flask application. 
The application analyzes 30 different financial features to make real-time approval decisions.

## Features
- **Machine Learning Integration**: Uses a trained Random Forest classifier with `StandardScaler` preprocessing to evaluate inputs.
- **Dynamic Form Generation**: The prediction form dynamically handles all features used in the notebook.
- **Modern UI**: Features a clean, responsive, and animated glassmorphism user interface built with Bootstrap 5 and custom CSS.
- **Flask Backend**: A lightweight, robust Flask server handling the model loading, scaling, and prediction logic.

## Folder Structure
```
Credit-Card-Approval/
│
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── model.pkl               # Saved Machine Learning Model
├── scaler.pkl              # Saved Preprocessing Scaler
├── README.md               # Project Documentation
│
├── templates/              # HTML Templates
│      home.html            # Landing page
│      index.html           # Prediction form
│      result.html          # Prediction result page
│
├── static/                 # Static Assets
│      css/
│          style.css        # Custom styles
│      images/              # (Optional) Image assets
│
└── Credit Card Approval Prediction.ipynb  # Original ML Notebook
```

## Installation

1. **Clone the repository or navigate to the directory**:
   ```bash
   cd "Credit Card Approval"
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Run Application

1. **Start the Flask server**:
   ```bash
   python app.py
   ```

2. **Open your browser** and navigate to:
   ```text
   http://127.0.0.1:5000
   ```

## Screenshots
![Home Page Placeholder](placeholder_home.png)
*Modern Hero Section*

![Prediction Form Placeholder](placeholder_form.png)
*Dynamic Feature Input Form*

![Result Page Placeholder](placeholder_result.png)
*Prediction Result Card*
