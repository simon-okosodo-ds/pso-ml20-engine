import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

# ============================================================
# 🧠 LOAD TRAINED PIPELINE
# ============================================================
MODEL_PATH = "models/valuation_pipeline.pkl"

@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):
        return None
    return joblib.load(MODEL_PATH)

model = load_model()

if model is None:
    st.error("❌ Model not found. Check valuation_pipeline.pkl path.")
    st.stop()

st.title("🏠 Property Valuation Engine")
st.write("ML Pipeline Inference (Notebook-Exact Behavior)")

# ============================================================
# 🧾 INPUT FORM (MUST MATCH TRAINING FEATURES)
# ============================================================
sqft = st.number_input("SqFt Living", 200, 25000, 1500)
grade = st.selectbox("Grade", ["Basic/Standard", "Modern/Executive", "Luxury/High-End", "Elite/Mansion"])
yr_built = st.number_input("Year Built", 1800, 2026, 2005)
bedrooms = st.number_input("Bedrooms", 0, 30, 3)
bathrooms = st.number_input("Bathrooms", 0, 20, 2)
sqft_lot = st.number_input("Lot Size", 500, 50000, 5000)
zipcode = st.number_input("ZipCode", 98001)

# ============================================================
# 🧠 ENCODING (ONLY IF YOU USED IT IN TRAINING)
# ============================================================
grade_map = {
    "Basic/Standard": 5,
    "Modern/Executive": 7,
    "Luxury/High-End": 9,
    "Elite/Mansion": 11
}

bldg_grade = grade_map[grade]

# ============================================================
# 🧾 BUILD INPUT DATAFRAME (NO FEATURE ENGINEERING)
# ============================================================
input_df = pd.DataFrame([{
    "SqFtTotLiving": sqft,
    "BldgGrade": bldg_grade,
    "YrBuilt": yr_built,
    "Bedrooms": bedrooms,
    "Bathrooms": bathrooms,
    "SqFtLot": sqft_lot,
    "ZipCode": zipcode
}])

# ============================================================
# 🔮 PREDICTION
# ============================================================
if st.button("Predict Price"):

    try:
        pred = model.predict(input_df)

        # Handle log models safely
        pred_value = pred[0]

        # Only convert if model was trained on log scale
        if pred_value < 20:
            price = np.expm1(pred_value)
        else:
            price = pred_value

        st.success(f"🏡 Estimated Price: ${price:,.2f}")

    except Exception as e:
        st.error("❌ Prediction failed")
        st.exception(e)

# ============================================================
# 🔍 DEBUG VIEW (VERY IMPORTANT FOR CLIENT TRUST)
# ============================================================
with st.expander("View Model Input"):
    st.dataframe(input_df)
