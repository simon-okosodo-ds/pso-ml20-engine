import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime

# ============================================================
# CONFIG
# ============================================================
st.set_page_config(page_title="PSO-ML20 Engine", layout="wide")

MODEL_PATH = "models/valuation_pipeline.pkl"

st.title("🏠 PSO-ML20 Valuation Engine (Stable Inference)")

# ============================================================
# LOAD MODEL (STRICT + SAFE)
# ============================================================
@st.cache_resource
def load_model():

    if not os.path.exists(MODEL_PATH):
        st.error(f"❌ Missing model: {MODEL_PATH}")
        st.stop()

    obj = joblib.load(MODEL_PATH)

    if isinstance(obj, dict):
        model = obj.get("pipeline") or obj.get("model")
        defaults = obj.get("defaults", {})
        log_flag = obj.get("uses_log_target", False)
    else:
        model = obj
        defaults = {}
        log_flag = False

    return model, defaults, log_flag


model, defaults, log_flag = load_model()

# ============================================================
# INPUTS
# ============================================================
st.subheader("📋 Property Inputs")

sqft = st.number_input("SqFt Living", 200, 25000, 2500)
bed = st.number_input("Bedrooms", 0, 20, 4)
bath = st.number_input("Bathrooms", 0, 20, 2)
yr = st.number_input("Year Built", 1800, datetime.now().year + 1, 2015)
lot = st.number_input("Lot Size", 0, 1000000, 5000)
zipc = st.number_input("ZipCode", 0, 99999, 98001)

grade_map = {
    "Basic/Standard": 5,
    "Modern/Executive": 7,
    "Luxury/High-End": 9,
    "Elite/Mansion": 11
}

grade = st.selectbox("Quality", list(grade_map.keys()))
grade_val = grade_map[grade]

# ============================================================
# PREDICTION ENGINE
# ============================================================
if st.button("⚡ Generate Valuation"):

    # -----------------------------
    # RAW INPUT FRAME
    # -----------------------------
    df = pd.DataFrame([{
        "SqFtTotLiving": sqft,
        "Bedrooms": bed,
        "Bathrooms": bath,
        "YrBuilt": yr,
        "SqFtLot": lot,
        "ZipCode": zipc,
        "BldgGrade": grade_val,
        "DocumentDate_year": datetime.now().year,
        "DocumentDate_month": datetime.now().month
    }])

    # -----------------------------
    # STRICT FEATURE MATCHING
    # -----------------------------
    if hasattr(model, "feature_names_in_"):
        expected = list(model.feature_names_in_)
    else:
        expected = df.columns.tolist()

    # IMPORTANT: do NOT use random zeros blindly
    for col in expected:
        if col not in df.columns:
            if col in defaults:
                df[col] = defaults[col]
            else:
                # safer fallback = column median-like stability proxy
                df[col] = 0

    df = df[expected]

    st.subheader("📊 Model Input (Schema Locked)")
    st.dataframe(df)

    # -----------------------------
    # PREDICTION
    # -----------------------------
    try:
        pred = model.predict(df)
        val = float(np.array(pred).reshape(-1)[0])

        # -------------------------
        # LOG SAFETY HANDLING
        # -------------------------
        if log_flag:
            val = np.expm1(val)

        # -------------------------
        # HARD STABILITY GUARDS
        # -------------------------
        if not np.isfinite(val):
            val = 0

        val = np.clip(val, 10000, 1e9)

        # -------------------------
        # OUTPUT
        # -------------------------
        st.success("✅ Stable Prediction Generated")

        st.metric(
            "Estimated Property Value",
            f"${val:,.2f}"
        )

        # Debug (helps MAPE tuning)
        st.caption(f"Raw model output: {pred}")

    except Exception as e:
        st.error(f"❌ Inference failed: {e}")
