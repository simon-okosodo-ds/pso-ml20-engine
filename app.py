import streamlit as st
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime
from xgboost import XGBRegressor

st.title("PSO-ML20 Automated Inference Engine")

# ============================================================
# 🛡️ 1. AUTOMATED TEXT-CORE PIPELINE INGESTION (0% PARSING RISK)
# ============================================================
repo_pkl = os.path.join(os.path.dirname(__file__) if '__file__' in locals() else ".", "models", "valuation_pipeline.pkl")

if not os.path.exists(repo_pkl):
    st.error("Missing core asset file: models/valuation_pipeline.pkl")
    st.stop()

try:
    # 🟢 THE REAL UNLOCK: Reads your file strictly as a safe alphanumeric text string layout
    with open(repo_pkl, "r", encoding="utf-8") as f:
        armor_text_string = f.read().strip()
        
    # Unpack the Base64 layer straight back into a binary memory stream
    decoded_binary_bytes = base64.b64decode(armor_text_string.encode("utf-8"))
    
    # Temporarily drop payload bytes to a safe cache file to allow joblib loading sequence
    temp_cache_path = "temp_runtime_asset.pkl"
    with open(temp_cache_path, "wb") as f:
        f.write(decoded_binary_bytes)
        
    loaded_asset = joblib.load(temp_cache_path)
    
    production_pipeline = loaded_asset.get("pipeline")
    training_defaults = loaded_asset.get("defaults", {})
    model_uses_log_target = loaded_asset.get("uses_log_target", True)
    
    # Clean up the cache file immediately to maintain data purity
    if os.path.exists(temp_cache_path):
        os.remove(temp_cache_path)
        
    expected_features = list(production_pipeline.feature_names_in_)
    
except Exception as parse_err:
    st.error(f"❌ MLOps SEVERE CONFIGURATION ERROR: Failed to decode text armor bundle. Trace: {parse_err}")
    st.stop()


# ============================================================
# 📄 2. DYNAMIC FRONTEND GENERATOR (NO HARDCODED INPUT BOXES)
# ============================================================
system_mode = st.radio("Pipeline Mode", ["Historical Validation Base", "Live Modern Market Base"])

st.markdown("### 📄 Model Feature Input Matrix")
user_inputs_map = {}

for feature in expected_features:
    default_val = training_defaults.get(feature, 0.0)
    if isinstance(default_val, (int, np.integer)):
        user_inputs_map[feature] = st.number_input(f"Input [Integer] -> {feature}", value=int(default_val))
    elif isinstance(default_val, (float, np.floating)):
        user_inputs_map[feature] = st.number_input(f"Input [Float] -> {feature}", value=float(default_val))
    else:
        user_inputs_map[feature] = st.text_input(f"Input [Text/Category] -> {feature}", value=str(default_val))

if 'DocumentDate_year' in expected_features:
    user_inputs_map['DocumentDate_year'] = 2015 if "Validation" in system_mode else datetime.now().year
if 'DocumentDate_month' in expected_features:
    user_inputs_map['DocumentDate_month'] = datetime.now().month

# ============================================================
# ⚡ 3. PURE PIPELINE INFERENCE EXECUTION
# ============================================================
st.markdown("<br>", unsafe_allow_html=True)
if st.button("RUN PURE PIPELINE INFERENCE"):
    
    inference_df = pd.DataFrame([user_inputs_map])[expected_features]
    st.write("Inference Input Data Vector Frame:")
    st.dataframe(inference_df)
    
    try:
        prediction_vector = production_pipeline.predict(inference_df)
        raw_prediction = float(prediction_vector) if isinstance(prediction_vector, (np.ndarray, list)) else float(prediction_vector)
        
        final_output_price = float(np.expm1(raw_prediction)) if model_uses_log_target else raw_prediction
        
        if "Live Modern Market" in system_mode:
            years_drift = max(datetime.now().year - 2015, 0)
            final_output_price = final_output_price * (1.028 ** years_drift)
            
        st.metric(label="🏆 CERTIFIED VALUATION RESULTS", value=f"${final_output_price:,.2f}")
        
    except Exception as e:
        st.error(f"❌ PIPELINE EXECUTION CRASH: Core inference failed. Trace: {e}")
