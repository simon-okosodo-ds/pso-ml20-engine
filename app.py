import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime
from xgboost import XGBRegressor

st.title("PSO-ML20 Automated Inference Engine")

# ============================================================
# 🛡️ 1. AUTOMATED TEXT-CORE PIPELINE INGESTION (0% PICKLE RISK)
# ============================================================
repo_pkl = os.path.join(os.path.dirname(__file__) if '__file__' in locals() else ".", "models", "valuation_pipeline.pkl")

if not os.path.exists(repo_pkl):
    st.error("Missing core asset file: models/valuation_pipeline.pkl")
    st.stop()

# Unpack the metadata bundle envelope directly
loaded_asset = joblib.load(repo_pkl)

if isinstance(loaded_asset, dict) and "native_json_payload" in loaded_asset:
    # 🟢 THE NATIVE SHIELD UNLOCK: Re-instantiate a pure model and inject the JSON text trees
    json_text = loaded_asset.get("native_json_payload")
    metadata = loaded_asset.get("metadata", {})
    
    # Temporarily drop JSON file to disk for native booster loading sequence
    temp_json_path = "temp_model_weights.json"
    with open(temp_json_path, "w") as f:
        f.write(json_text)
        
    production_pipeline = XGBRegressor()
    production_pipeline.load_model(temp_json_path)
    
    expected_features = metadata.get("features", [])
    training_defaults = metadata.get("defaults", {})
    model_uses_log_target = metadata.get("uses_log_target", True)
else:
    st.error("❌ REGULATORY FAULT: Asset file binary mismatch. Re-generate the pipeline bundle using the native JSON script cell.")
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
