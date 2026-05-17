import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime

st.title("PSO-ML20 Automated Inference Engine")

# ============================================================
# 🛡️ 1. AUTOMATED PIPELINE BUNDLE INGESTION (0% HARDCODED)
# ============================================================
repo_pkl = os.path.join(os.path.dirname(__file__) if '__file__' in locals() else ".", "models", "valuation_pipeline.pkl")

if not os.path.exists(repo_pkl):
    st.error("Missing core asset file: models/valuation_pipeline.pkl")
    st.stop()

# Unpack the binary container directly into active system memory
loaded_asset = joblib.load(repo_pkl)
production_pipeline = loaded_asset.get("pipeline")
training_defaults = loaded_asset.get("defaults", {})
model_uses_log_target = loaded_asset.get("uses_log_target", True)

# Enforce a strict schema lock checking
if not hasattr(production_pipeline, 'feature_names_in_'):
    st.error("Severe Error: Model file is not schema-locked. Rebuild your notebook pipeline bundle.")
    st.stop()

# 🧠 THE DYNAMIC SNIFFER: Automatically sniffs the exact features your model expects
expected_features = list(production_pipeline.feature_names_in_)

# ============================================================
# 📄 2. DYNAMIC FRONTEND GENERATOR (NO HARDCODED INPUT BOXES)
# ============================================================
system_mode = st.radio("Pipeline Mode", ["Historical Validation Base", "Live Modern Market Base"])

st.markdown("### 📄 Model Feature Input Matrix")
user_inputs_map = {}

# Loop through the sniffed columns list and dynamically build a matching UI box for each
for feature in expected_features:
    # Check if the notebook saved a valid training baseline value for this feature column
    default_val = training_defaults.get(feature, 0.0)
    
    # Cast formatting based on numeric signatures to keep datatypes aligned
    if isinstance(default_val, (int, np.integer)):
        user_inputs_map[feature] = st.number_input(f"Input [Integer] -> {feature}", value=int(default_val))
    elif isinstance(default_val, (float, np.floating)):
        user_inputs_map[feature] = st.number_input(f"Input [Float] -> {feature}", value=float(default_val))
    else:
        user_inputs_map[feature] = st.text_input(f"Input [Text/Category] -> {feature}", value=str(default_val))

# Override date targets explicitly based on your sidebar mode selection
if 'DocumentDate_year' in expected_features:
    user_inputs_map['DocumentDate_year'] = 2015 if "Validation" in system_mode else datetime.now().year
if 'DocumentDate_month' in expected_features:
    user_inputs_map['DocumentDate_month'] = datetime.now().month

# ============================================================
# ⚡ 3. PURE PIPELINE INFERENCE EXECUTION
# ============================================================
st.markdown("<br>", unsafe_allow_html=True)
if st.button("RUN PURE PIPELINE INFERENCE"):
    
    # Pack parameters inside the clean dataframe structure matching the index sequence perfectly
    inference_df = pd.DataFrame([user_inputs_map])[expected_features]
    
    # Renders the exact input vector audit matrix table reaching your model
    st.write("📊 **Strict Production Inference Audit Input Log Frame:**")
    st.dataframe(inference_df)
    
    try:
        prediction_vector = production_pipeline.predict(inference_df)
        raw_prediction = float(prediction_vector) if isinstance(prediction_vector, (np.ndarray, list)) else float(prediction_vector)
        
        # Reverse log transforms natively if target was evaluated via log1p
        final_output_price = float(np.expm1(raw_prediction)) if model_uses_log_target else raw_prediction
        
        # Apply downstream temporal growth indexing only if running Live Market Mode
        if "Live Modern Market" in system_mode:
            years_drift = max(datetime.now().year - 2015, 0)
            final_output_price = final_output_price * (1.028 ** years_drift)
            
        # Display the pure calculation scalar output natively using a standard metric element
        st.metric(label="🏆 CERTIFIED VALUATION RESULTS", value=f"${final_output_price:,.2f}")
        
    except Exception as e:
        st.error(f"❌ PIPELINE EXECUTION CRASH: Core inference failed. Trace: {e}")
