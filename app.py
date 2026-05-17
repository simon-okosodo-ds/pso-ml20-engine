# ============================================================
# PSO-ML20 STREAMLIT APP — CLEAN PRODUCTION VERSION
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

from datetime import datetime

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="PSO-ML20 Valuation Engine",
    page_icon="🏠",
    layout="wide"
)

# ============================================================
# TITLE
# ============================================================

st.title("🏠 PSO-ML20 Real Estate Valuation Engine")
st.caption("Production Pipeline Inference System")

# ============================================================
# MODEL PATH
# ============================================================

MODEL_PATH = "valuation_pipeline.pkl"

# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_pipeline():

    if not os.path.exists(MODEL_PATH):
        st.error("❌ valuation_pipeline.pkl not found in GitHub root folder.")
        st.stop()

    try:
        loaded_asset = joblib.load(MODEL_PATH)

        # ----------------------------------------------------
        # IF PKL IS METADATA BUNDLE
        # ----------------------------------------------------

        if isinstance(loaded_asset, dict):

            pipeline_object = loaded_asset.get("pipeline")

            training_defaults = loaded_asset.get("defaults", {})

            model_uses_log_target = loaded_asset.get(
                "uses_log_target",
                True
            )

        # ----------------------------------------------------
        # IF PKL IS NORMAL PIPELINE
        # ----------------------------------------------------

        else:

            pipeline_object = loaded_asset

            model_uses_log_target = True

            training_defaults = {}

        return (
            pipeline_object,
            training_defaults,
            model_uses_log_target
        )

    except Exception as e:

        st.error(f"❌ PKL LOAD FAILURE:\n\n{e}")

        st.stop()

# ============================================================
# LOAD ASSETS
# ============================================================

pipeline_object, training_defaults, model_uses_log_target = load_pipeline()

# ============================================================
# INPUT UI
# ============================================================

st.subheader("📋 Property Inputs")

c1, c2, c3 = st.columns(3)

with c1:
    sqft = st.number_input(
        "SqFt Living Area",
        min_value=200,
        max_value=25000,
        value=2500,
        step=50
    )

with c2:
    bedrooms = st.number_input(
        "Bedrooms",
        min_value=0,
        max_value=20,
        value=4
    )

with c3:
    bathrooms = st.number_input(
        "Bathrooms",
        min_value=0,
        max_value=20,
        value=2
    )

c4, c5, c6 = st.columns(3)

with c4:
    yr_built = st.number_input(
        "Year Built",
        min_value=1800,
        max_value=datetime.now().year + 1,
        value=2015
    )

with c5:
    sqft_lot = st.number_input(
        "Lot Size",
        min_value=0,
        max_value=1000000,
        value=5000
    )

with c6:
    zipcode = st.number_input(
        "ZipCode",
        min_value=0,
        max_value=99999,
        value=98001
    )

build_type = st.selectbox(
    "Quality Category",
    [
        "Basic/Standard",
        "Modern/Executive",
        "Luxury/High-End",
        "Elite/Mansion"
    ]
)

# ============================================================
# GRADE MAPPING
# ============================================================

grade_mapping = {
    "Basic/Standard": 5,
    "Modern/Executive": 7,
    "Luxury/High-End": 9,
    "Elite/Mansion": 11
}

numeric_grade = grade_mapping.get(build_type, 7)

# ============================================================
# PREDICT BUTTON
# ============================================================

predict_btn = st.button(
    "⚡ GENERATE VALUATION",
    use_container_width=True
)

# ============================================================
# PREDICTION ENGINE
# ============================================================

if predict_btn:

    try:

        # ----------------------------------------------------
        # BUILD RAW INPUT DATAFRAME
        # ----------------------------------------------------

        raw_user_df = pd.DataFrame([{

            "SqFtTotLiving": sqft,
            "Bedrooms": bedrooms,
            "Bathrooms": bathrooms,
            "YrBuilt": yr_built,
            "SqFtLot": sqft_lot,
            "ZipCode": zipcode,
            "BldgGrade": numeric_grade,
            "DocumentDate_year": datetime.now().year,
            "DocumentDate_month": datetime.now().month

        }])

        # ----------------------------------------------------
        # GET EXPECTED FEATURES
        # ----------------------------------------------------

        if hasattr(pipeline_object, "feature_names_in_"):

            expected_cols = list(
                pipeline_object.feature_names_in_
            )

        else:

            expected_cols = list(raw_user_df.columns)

        # ----------------------------------------------------
        # FILL MISSING FEATURES
        # ----------------------------------------------------

        for col in expected_cols:

            if col not in raw_user_df.columns:

                if col in training_defaults:

                    raw_user_df[col] = training_defaults[col]

                else:

                    raw_user_df[col] = 0

        # ----------------------------------------------------
        # STRICT COLUMN ORDER
        # ----------------------------------------------------

        raw_user_df = raw_user_df[expected_cols]

        # ----------------------------------------------------
        # SHOW AUDIT FRAME
        # ----------------------------------------------------

        st.subheader("📊 Production Audit Frame")

        st.dataframe(
            raw_user_df,
            use_container_width=True
        )

        # ----------------------------------------------------
        # PREDICT
        # ----------------------------------------------------

        pred = pipeline_object.predict(raw_user_df)

        raw_val = float(pred[0])

        # ----------------------------------------------------
        # LOG TARGET FIX
        # ----------------------------------------------------

        if model_uses_log_target:

            prediction = float(np.expm1(raw_val))

        else:

            prediction = raw_val

        # ----------------------------------------------------
        # SAFETY FLOOR
        # ----------------------------------------------------

        prediction = max(prediction, 10000)

        # ----------------------------------------------------
        # RESULT UI
        # ----------------------------------------------------

        st.success("✅ Prediction Complete")

        st.markdown("---")

        st.metric(
            "🏠 Estimated Property Value",
            f"${prediction:,.2f}"
        )

    except Exception as e:

        st.error(f"❌ INFERENCE FAILURE:\n\n{e}")
