# Credit Card Approval Prediction

A complete end-to-end Machine Learning web application for predicting Credit Card Approvals.
Built with Flask and a Random Forest classifier, styled with the **SmartBridge** interface.

---

## Features
- **SmartBridge UI** — Clean form with dropdowns matching real credit card application fields
- **Random Forest Model** — Trained on 14 demographic and financial features
- **Result Page** — Shows Approved / Rejected with model confidence percentage
- **Auto Model Training** — If pkl files are missing, `start.bat` trains the model automatically

---

## Folder Structure
```
Skill-Wallet-Project/
│
├── app.py                  # Main Flask application
├── train_model.py          # Model training script (run once to generate pkl files)
├── model.pkl               # Trained Random Forest model
├── scaler.pkl              # StandardScaler for preprocessing
├── requirements.txt        # Python dependencies
├── Procfile                # Render deployment config
├── render.yaml             # Render one-click deploy config
├── start.bat               # Windows local launcher
├── README.md               # Project documentation
│
├── templates/
│   ├── index.html          # SmartBridge prediction form
│   └── result.html         # Prediction result page
│
└── Credit Card Approval Prediction.ipynb   # Original ML Notebook
```

---

## Run Locally (Windows)

Just double-click `start.bat` — it handles everything automatically:
1. Creates virtual environment
2. Installs dependencies
3. Trains model if missing
4. Opens browser at http://127.0.0.1:5000

Or manually:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python train_model.py      # only needed once
python app.py
```

---

## Deploy on Render

### Option A — One-click (using render.yaml)
1. Push this repo to GitHub
2. Go to [render.com](https://render.com) → **New** → **Blueprint**
3. Connect your GitHub repo → Render auto-reads `render.yaml` → Deploy

### Option B — Manual setup
1. Go to [render.com](https://render.com) → **New** → **Web Service**
2. Connect your GitHub repo
3. Fill in these settings:

| Setting | Value |
|---|---|
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt && python train_model.py` |
| **Start Command** | `gunicorn app:app` |
| **Plan** | Free |

4. Click **Deploy** — your app will be live in ~2 minutes!

---

## Input Fields

| Field | Type | Example |
|---|---|---|
| Gender | Dropdown | MALE / FEMALE |
| Own Car | Dropdown | YES / NO |
| Own Realstate | Dropdown | YES / NO |
| Total Annual Income | Number | 200000 |
| Type of Income | Dropdown | Working, Pensioner, etc. |
| Education | Dropdown | Higher education, etc. |
| Family Status | Dropdown | Married, Single, etc. |
| Type of Housing | Dropdown | House / apartment, etc. |
| Days Birth | Number (age in years) | 35 |
| Days Employed | Number (negative = employed) | -10 |
| Family Members | Number | 3 |
| EMI Paid Off | Number | 10 |
| EMI of Past Dues | Number | 0 |
| Number of Loans | Number | 2 |

## Values for Approved Result
- Annual Income **> 100,000**
- Own Realstate = **YES**
- EMI of Past Dues = **0**
