"""
Train the Credit Card Approval Prediction model.
Run this script once to generate model.pkl and scaler.pkl before starting the app.
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pickle
import os

print("Training Credit Card Approval model...")

np.random.seed(42)
n_samples = 5000

# Simulate a credit card approval dataset matching the SmartBridge interface fields
gender          = np.random.randint(0, 2, n_samples)           # 0=F, 1=M
own_car         = np.random.randint(0, 2, n_samples)           # 0=N, 1=Y
own_realty      = np.random.randint(0, 2, n_samples)           # 0=N, 1=Y
income          = np.random.uniform(20000, 500000, n_samples)  # annual income
income_type     = np.random.randint(0, 5, n_samples)           # 0-4 encoded
education       = np.random.randint(0, 5, n_samples)           # 0-4 encoded
family_status   = np.random.randint(0, 5, n_samples)           # 0-4 encoded
housing_type    = np.random.randint(0, 6, n_samples)           # 0-5 encoded
days_birth      = np.random.uniform(20, 70, n_samples)         # age in years approx
days_employed   = np.random.uniform(-20, 0, n_samples)         # years employed (negative)
family_members  = np.random.randint(1, 7, n_samples)           # 1-6
emi_paid_off    = np.random.randint(0, 20, n_samples)          # EMIs paid
emi_pastdues    = np.random.randint(0, 10, n_samples)          # past due EMIs
num_loans       = np.random.randint(0, 10, n_samples)          # number of loans

# Approval business logic
approved = (
    (income > 100000) & (emi_pastdues < 3) & (own_realty == 1)
).astype(int)

# Add 15% noise for realism
noise = np.random.rand(n_samples) < 0.15
approved = np.where(noise, 1 - approved, approved)

X = np.column_stack([
    gender, own_car, own_realty, income, income_type, education,
    family_status, housing_type, days_birth, days_employed,
    family_members, emi_paid_off, emi_pastdues, num_loans
])
y = approved

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc  = scaler.transform(X_test)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight='balanced',
    n_jobs=-1
)
model.fit(X_train_sc, y_train)

accuracy = model.score(X_test_sc, y_test)
print(f"Model Accuracy: {accuracy:.4f}")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, 'model.pkl'), 'wb') as f:
    pickle.dump(model, f)
with open(os.path.join(BASE_DIR, 'scaler.pkl'), 'wb') as f:
    pickle.dump(scaler, f)

print("model.pkl and scaler.pkl saved successfully!")
print("You can now start the app.")
