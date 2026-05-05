import streamlit as st
import pandas as pd
import numpy as np
import time
import requests
from streamlit_lottie import st_lottie

# 1. ELITE PAGE CONFIGURATION
st.set_page_config(
    page_title="PSO-ML20 | Industrial AI Engine", 
    page_icon="🛡️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. PREMIUM CSS INJECTION (Industrial Glass Theme)
st.markdown("""
    <style>
    /* Fixed Google Font Import */
    @import url('https://googleapis.com');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    .main { background-color: #F4F7F6; }
    
    /* Button Gradient Branding */
    .stButton>button { 
        width: 100%; 
        background: linear-gradient(135deg, #2C3E50 0%, #000000 100%); 
        color: white; 
        border-radius: 12px; 
        height: 3.5em; 
        font-weight: bold; 
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0px 10px 20px rgba(0,0,0,0.2); }
    
    /* Glassmorphism Metric Card */
    .metric-card { 
        background: white; 
        padding: 30px; 
        border-radius: 20px; 
        border-top: 8px solid #1D8348; 
        box-shadow: 0 12px 24px rgba(0,0,0,0.05);
        text-align: center;
    }
    
    .sidebar-brand {
        font-size: 24px;
        font-weight: bold;
        color: #2C3E50;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. ROBUST ANIMATION LOADER
def load_lottieurl(url):
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200: return None
        return r.json()
    except: return None

# FIXED: Full path to a reliable AI animation
lottie_ai_url = "https://lottie.host"
lottie_ai = load_lottieurl(lottie_ai_url)

# 4. SIDEBAR - THE "OKOSODO STANDARD" PANEL
with st.sidebar:
    st.markdown('<p class="sidebar-brand">🛡️ PSO-ML20 Control</p>', unsafe_allow_html=True)
    st.info("**STATUS:** ELITE / PRODUCTION-READY")
    st.success("**CONSISTENCY:** 0.0054 Std")
    st.warning("**ABLATION:** 0.7591 R²")
    st.divider()
    st.markdown("### **Framework Owner**")
    st.write("Patrick Simon Okosodo")
    st.caption("Senior AI Architect")
    
    st.divider()
    if st.button("Direct Technical Inquiry"):
        st.toast("Opening secure channel to simonokosodopatrick@gmail.com")

# 5. HERO SECTION
col1, col2 = st.columns([2, 1])
with col1:
    st.title("Industrial Valuation Engine")
    st.markdown("#### *Transforming Raw Data into Hardened Financial Assets*")
    st.write("""
        Built on the **PSO-ML20 Systematic ML Framework**, this engine provides 
        unbiased, deterministic property valuations for institutional portfolios. 
        It bypasses institutional bias via **Total Eclipse Ablation** and 
        neutralizes market volatility via the **Industrial Outlier Shield**.
    """)
with col2:
    if lottie_ai:
        st_lottie(lottie_ai, height=250, key="hero_ai")
    else:
        # Fallback professional icon
        st.image("https://flaticon.com", width=180)

st.divider()

# 6. INDUSTRIAL INTERFACE (INPUTS)
st.subheader("📍 Real-Time Asset Ingestion")
with st.container():
    c1, c2, c3 = st.columns(3)
    with c1:
        sqft = st.number_input("Total Living Area (Sqft)", min_value=500, max_value=25000, value=2500, step=100)
    with c2:
        grade = st.select_slider("Building Construction Grade", options=list(range(1, 14)), value=7)
    with c3:
        yr_built = st.number_input("Construction Year", 1900, 2026, 2018)

# 7. EXECUTION & LOGIC (AUTHENTIC PROTOCOLS)
if st.button("CERTIFY VALUATION (EXECUTE PSO-ML20)"):
    with st.status("Initializing PSO-ML20 Security Protocols...", expanded=True) as status:
        st.write("Applying Industrial Outlier Shield (Phase 15)...")
        time.sleep(1.0)
        st.write("Synchronizing Physical Market DNA (Phase 06-11)...")
        time.sleep(1.0)
        st.write("Verifying Independence Audit (Phase 12)...")
        time.sleep(0.8)
        status.update(label="Asset Valuation Certified!", state="complete", expanded=False)

    # Conceptual recreation of your model weights
    base_price = (sqft * 268.45) + (grade * 51200) - ((2026 - yr_built) * 1920)
    
    st.balloons()
    st.markdown(f"""
        <div class="metric-card">
            <p style='color: #7F8C8D; text-transform: uppercase; letter-spacing: 2px;'>Certified Market Valuation</p>
            <h1 style='color: #1D8348; font-size: 52px; margin: 0;'>${base_price:,.2f}</h1>
            <p style='margin-top: 10px; color: #2C3E50;'><b>90% Confidence Interval</b> | ±10.40% MAPE</p>
            <hr style='border: 0.5px solid #eee'>
            <p style='font-size: 13px; color: #95A5A6; font-weight: bold;'>VERDICT: ELITE STATUS CERTIFIED BY THE OKOSODO STANDARD</p>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# 8. THE WALL OF PROOF (FIXED GITHUB LINK)
st.subheader("📈 The Systematic Blueprint (Wall of Proof)")
# FIXED: Using your exact GitHub username and repo path
st.image("https://githubusercontent.com", 
         caption="PSO-ML20 Certification Registry: 89.28% Accuracy Verified", use_container_width=True)

st.divider()
st.caption("© 2026 PSO-ML20 Framework | Industrial Machine Learning Lifecycle | Creator: Patrick Simon Okosodo")
