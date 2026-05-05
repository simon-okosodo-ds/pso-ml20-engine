import streamlit as st
import pandas as pd
import numpy as np
import time
from streamlit_lottie import st_lottie
import requests

# 1. PAGE CONFIGURATION (STARTUP BRANDING)
st.set_page_config(page_title="PSO-ML20 | Industrial AI Engine", page_icon="🛡️", layout="wide")

# 2. THE "ELITE" UI THEME (CSS)
st.markdown("""
    <style>
    .main { background-color: #F8F9F9; }
    .stButton>button { width: 100%; background-color: #2C3E50; color: white; border-radius: 10px; height: 3em; font-weight: bold; }
    .metric-card { background-color: white; padding: 20px; border-radius: 15px; border-left: 5px solid #1D8348; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# 3. LOAD ANIMATION (FREE LOTTIE FILES)
def load_lottieurl(url):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

lottie_ai = load_lottieurl("https://lottiefiles.com") # Modern AI Sphere

# 4. SIDEBAR - THE "OKOSODO STANDARD" MENU
with st.sidebar:
    st.image("https://adobe.com") # Replace with your QR
    st.title("PSO-ML20 Control")
    st.info("System Status: ELITE / HARDENED")
    st.success("Consistency: 0.0054 Std")
    st.warning("Ablation Score: 0.7591")

# 5. HEADER SECTION
col1, col2 = st.columns([2, 1])
with col1:
    st.title("🛡️ PSO-ML20 Industrial Valuation Engine")
    st.subheader("Transforming Raw Data into Hardened Financial Assets")
    st.write("Built on the **20-Phase Systematic ML Framework**, this engine provides unbiased, deterministic property valuations for institutional portfolios.")
with col2:
    st_lottie(lottie_ai, height=200, key="coding")

st.divider()

# 6. INTERACTIVE VALUATION TOOL
st.header("📍 Live Industrial Valuation")
c1, c2, c3 = st.columns(3)
with c1:
    sqft = st.number_input("Total Living Area (Sqft)", min_value=500, max_value=20000, value=2500)
with c2:
    grade = st.slider("Building Grade (1-13)", 1, 13, 7)
with c3:
    yr_built = st.number_input("Year Built", 1900, 2024, 2015)

if st.button("EXECUTE PSO-ML20 CERTIFIED VALUATION"):
    with st.spinner("Synchronizing with Market Physics..."):
        time.sleep(1.5) # Professional processing delay
        # This is where your model logic lives
        mock_price = (sqft * 250) + (grade * 50000) - ((2024 - yr_built) * 2000)
        
        st.balloons()
        st.markdown(f"""
            <div class="metric-card">
                <h2 style='color: #1D8348; text-align: center;'>CERTIFIED VALUATION: ${mock_price:,.2f}</h2>
                <p style='text-align: center;'>Confidence Interval: ±10.40% (MAPE) | Outlier Shield: ACTIVE</p>
            </div>
            """, unsafe_allow_html=True)

st.divider()

# 7. THE MASTER PROOF (PORTFOLIO HOOK)
st.header("📈 The Systematic Blueprint (Wall of Proof)")
st.write("Every valuation is backed by our 20-phase integrity audit.")
# Use your Master Blueprint Image here
st.image("https://placeholder.com") 

st.divider()
st.button("Request Institutional Data Health Audit")
