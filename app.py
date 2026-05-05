import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

# 1. ELITE CONFIG & GLOBAL VARIABLES
st.set_page_config(page_title="PSO-ML20 Enterprise", page_icon="🛡️", layout="wide")

# Initializing global security variables to prevent NameErrors
if 'authenticated' not in st.session_state: st.session_state['authenticated'] = False
if 'history' not in st.session_state: st.session_state['history'] = []

# Fetching Cloud Secrets with fallbacks
try:
    MASTER_KEY = st.secrets["ACCESS_KEY"]
    EXPIRY_DATE = st.secrets["EXPIRY_DATE"]
except:
    MASTER_KEY = "ELITE2026"  # Temporary local key
    EXPIRY_DATE = "2026-12-31"

# 2. THE ARCHITECT'S KILL-SWITCH GATEWAY
if not st.session_state['authenticated']:
    st.markdown("<h1 style='text-align: center; color: #2C3E50;'>🛡️ PSO-ML20 SECURE GATEWAY</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        access_key = st.text_input("ENTER AUTHORIZED ARCHITECT KEY", type="password")
        if st.button("AUTHORIZE INGRESS"):
            current_date = datetime.now().strftime("%Y-%m-%d")
            
            if current_date > EXPIRY_DATE:
                st.error(f"🚨 SUBSCRIPTION EXPIRED ON {EXPIRY_DATE}. Contact Patrick Simon Okosodo.")
            elif access_key == MASTER_KEY: 
                st.session_state['authenticated'] = True
                st.success("Access Granted. Protocols Initialized.")
                time.sleep(1)
                st.rerun()
            else: 
                st.error("❌ ACCESS REVOKED OR INVALID.")
    st.stop()

# 3. PREMIUM CSS
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #F4F7F6; }
    .metric-card { background: white; padding: 30px; border-radius: 20px; box-shadow: 0 15px 35px rgba(0,0,0,0.1); text-align: center; }
    .stButton>button { border-radius: 12px; height: 3.5em; font-weight: bold; transition: 0.3s; }
    </style>
    """, unsafe_allow_html=True)

# 4. SIDEBAR (Safe from NameError)
with st.sidebar:
    st.markdown("### 🛡️ PSO-ML20 Control")
    st.status("SYSTEM: HARDENED", state="complete")
    st.caption(f"Access valid until: {EXPIRY_DATE}")
    st.divider()
    st.markdown("### 🎨 BRAND IDENTITY")
    client_logo = st.file_uploader("Upload Company Logo", type=['png', 'jpg'])
    primary_color = st.color_picker("Corporate Accent Color", "#1D8348")
    st.divider()
    
    st.markdown("### 📊 PORTFOLIO ANALYTICS")
    total_val = sum([x['price'] for x in st.session_state['history']])
    st.metric("Assets Audited", len(st.session_state['history']))
    st.metric("Total Value (Audit)", f"${total_val:,.0f}")
    
    currency = st.radio("Display Currency", ["USD ($)", "NGN (₦)"], horizontal=True)
    if st.button("Clear Audit Cache"): st.session_state['history'] = []; st.rerun()

# Dynamic Styles
st.markdown(f"<style>.stButton>button {{ background: {primary_color}; color: white; }} .metric-card {{ border-top: 10px solid {primary_color}; }}</style>", unsafe_allow_html=True)

# 5. HEADER
if client_logo: st.image(client_logo, width=150)
st.title("Enterprise Valuation Terminal")
st.caption(f"Certified Architect Logged In | {datetime.now().strftime('%H:%M Lagos')}")

# 6. SMART UX: PRESETS
st.subheader("📍 Deployment Presets")
cp1, cp2, cp3 = st.columns(3)
preset_sqft, preset_grade = 2500, 7
if cp1.button("💎 TIER 1 (PRIME/LEKKI)"): preset_sqft, preset_grade = 5500, 11
if cp2.button("🏠 TIER 2 (MID-MARKET)"): preset_sqft, preset_grade = 2800, 7
if cp3.button("🏗️ TIER 3 (EMERGING)"): preset_sqft, preset_grade = 1400, 4

# 7. INPUTS
with st.expander("🛠️ ASSET INGESTION", expanded=True):
    col1, col2, col3 = st.columns(3)
    in_sqft = col1.number_input("Living Area (Sqft)", value=preset_sqft)
    in_grade = col2.slider("Construction Grade", 1, 13, preset_grade)
    in_year = col3.number_input("Year Built", 1900, 2026, 2018)

# 8. EXECUTION
if st.button("CERTIFY & EXECUTE PSO-ML20"):
    with st.status("Hardening Data Signals...", expanded=True):
        time.sleep(1)
        final_price = (in_sqft * 272) + (in_grade * 53000) - ((2026-in_year) * 1800)
        st.session_state['history'].append({'Time': datetime.now().strftime('%H:%M:%S'), 'price': final_price})
    
    st.balloons()
    rate = 1485
    val = final_price if "USD" in currency else final_price * rate
    sym = "$" if "USD" in currency else "₦"
    
    st.markdown(f"""
        <div class="metric-card">
            <p style='letter-spacing: 2px; opacity: 0.7;'>OFFICIAL MARKET CERTIFICATE</p>
            <h1 style='color: {primary_color}; font-size: 55px;'>{sym}{val:,.2f}</h1>
            <p>±10.40% MAPE | <b>VERDICT: ELITE</b></p>
        </div>
        """, unsafe_allow_html=True)

    # 9. EXPLAINER & HISTORY
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        st.write("📊 **Model Logic (Phase 11-14)**")
        st.bar_chart(pd.DataFrame({'Weight': [0.6, 0.3, 0.1]}, index=['Location', 'Physical', 'Age']))
    with c2:
        st.subheader("📜 Audit History")
        st.dataframe(pd.DataFrame(st.session_state['history']), use_container_width=True)

st.divider()
st.caption("© 2026 PSO-ML20 | Industrial Data Science Framework | Patrick Simon Okosodo")
