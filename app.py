# ============================================================
# 🧠 REAL ESTATE VALUATION SAAS ARCHITECTURE (PRODUCTION READY)
# ============================================================

# =========================
# 📦 IMPORTS
# =========================
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import sqlite3
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import threading

# =========================
# 🧠 LOAD MODEL PIPELINE (SINGLE SOURCE OF TRUTH)
# =========================
PIPELINE_PATH = "valuation_pipeline.pkl"

@st.cache_resource
def load_pipeline():
    if not os.path.exists(PIPELINE_PATH):
        raise FileNotFoundError("Pipeline not found")
    return joblib.load(PIPELINE_PATH)

pipeline = load_pipeline()

# Detect log model safely
LOG_MODEL = True  # set this from notebook metadata if available

# =========================
# 🗄️ LIGHTWEIGHT DATABASE (SQLITE)
# =========================
conn = sqlite3.connect("predictions.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    sqft REAL,
    grade REAL,
    yr_built REAL,
    bedrooms REAL,
    bathrooms REAL,
    zip INTEGER,
    prediction REAL
)
""")
conn.commit()

def log_prediction(inputs, prediction):
    cursor.execute("""
        INSERT INTO predictions (
            timestamp, sqft, grade, yr_built, bedrooms, bathrooms, zip, prediction
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        str(datetime.now()),
        inputs["SqFtTotLiving"],
        inputs["BldgGrade"],
        inputs["YrBuilt"],
        inputs["Bedrooms"],
        inputs["Bathrooms"],
        inputs["ZipCode"],
        prediction
    ))
    conn.commit()

# =========================
# ⚙️ FASTAPI BACKEND (MODEL SERVICE)
# =========================
app = FastAPI(title="Valuation API")

class HouseInput(BaseModel):
    SqFtTotLiving: float
    BldgGrade: float
    YrBuilt: float
    Bedrooms: int
    Bathrooms: int
    SqFtLot: float
    ZipCode: int
    NbrLivingUnits: int
    DocumentDate_year: int
    DocumentDate_month: int

@app.post("/predict")
def predict(data: HouseInput):

    df = pd.DataFrame([data.dict()])

    pred = pipeline.predict(df)[0]

    if LOG_MODEL:
        pred = np.expm1(pred)

    return {"prediction": float(pred)}

def run_api():
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Run API in background thread (for Streamlit integration)
threading.Thread(target=run_api, daemon=True).start()

# =========================
# 🖥️ STREAMLIT FRONTEND (UI ONLY)
# =========================
st.title("🏠 Real Estate Valuation SaaS")

st.markdown("### Enter Property Details")

sqft = st.number_input("SqFtTotLiving", 200, 25000, 1200)
grade = st.number_input("BldgGrade", 1, 13, 7)
yr_built = st.number_input("YrBuilt", 1800, 2026, 2005)
bed = st.number_input("Bedrooms", 0, 10, 3)
bath = st.number_input("Bathrooms", 0, 10, 2)
lot = st.number_input("SqFtLot", 500, 50000, 5000)
zipcode = st.number_input("ZipCode", 10000, 99999, 98001)
units = st.number_input("NbrLivingUnits", 1, 10, 1)

if st.button("Predict Value"):

    # =========================
    # 🟢 RAW INPUT ONLY (NO ENGINEERING)
    # =========================
    user_df = pd.DataFrame([{
        "SqFtTotLiving": sqft,
        "BldgGrade": grade,
        "YrBuilt": yr_built,
        "Bedrooms": bed,
        "Bathrooms": bath,
        "SqFtLot": lot,
        "ZipCode": zipcode,
        "NbrLivingUnits": units,
        "DocumentDate_year": datetime.now().year,
        "DocumentDate_month": datetime.now().month
    }])

    # =========================
    # 🧠 DIRECT PIPELINE INFERENCE
    # =========================
    prediction = pipeline.predict(user_df)[0]

    if LOG_MODEL:
        prediction = np.expm1(prediction)

    prediction = max(prediction, 10000)  # safety floor

    # =========================
    # 💾 LOG RESULT (SAAS FEATURE)
    # =========================
    log_prediction(user_df.iloc[0].to_dict(), prediction)

    # =========================
    # 📊 OUTPUT
    # =========================
    st.success(f"Estimated Property Value: ${prediction:,.2f}")

    st.write("Logged to database ✔")

# =========================
# 📈 OPTIONAL: SIMPLE ANALYTICS PANEL
# =========================
if st.checkbox("Show prediction history"):

    df_logs = pd.read_sql_query("SELECT * FROM predictions", conn)
    st.dataframe(df_logs)

# ============================================================
# 🧠 END OF SAAS ARCHITECTURE
# ============================================================
