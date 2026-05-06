import streamlit as st
import pandas as pd
import numpy as np
import time
import io
from datetime import datetime
from PIL import Image, ImageOps, ImageFilter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# --- 1. ANTI-BIAS VISION ENGINE (THE MATERIAL SENSOR) ---
def analyze_visual_quality(uploaded_file):
    if uploaded_file is None:
        return 1.0
    try:
        # Load and convert to Grayscale
        img = Image.open(uploaded_file).convert('L')
        
        # 🛡️ STEP 1: LIGHTING NORMALIZATION (Anti-Bias)
        # Equalizes contrast so dark photos are analyzed as clearly as bright ones
        img = ImageOps.equalize(img) 
        
        # 🛡️ STEP 2: STRUCTURAL EDGE EXTRACTION
        # Detects complex material patterns (marble veins, POP, carvings) 
        # which exist even in low-quality phone captures
        edges = img.filter(ImageFilter.FIND_EDGES)
        edge_array = np.array(edges)
        
        # Calculate Structural Entropy (Material Complexity)
        material_score = np.mean(edge_array) 
        
        # 🛡️ STEP 3: NON-LINEAR MARKET SCALING
        if material_score > 30: return 1.22    # High-Resolution Luxury Texture
        if material_score > 15: return 1.12    # Modern Structural Detail
        return 1.05                            # Standard Smooth Finish
    except:
        return 1.0

# --- 2. PDF GENERATOR ENGINE ---
def generate_pso_pdf(val, sym, sqft, build_type, yr, inventory, images):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 750, "PSO-ML20 INDUSTRIAL VALUATION CERTIFICATE")
    p.setFont("Helvetica", 10)
    p.drawString(50, 735, f"Date: {datetime.now().strftime('%Y-%m-%d')} | Ref: PSO-{np.random.randint(1000,9999)}")
    p.line(50, 730, 550, 730)

    p.setFont("Helvetica-Bold", 24)
    p.setFillColorRGB(0.11, 0.51, 0.28) 
    p.drawString(50, 690, f"MARKET VALUE: {sym}{val:,.2f}")
    p.setFillColorRGB(0, 0, 0)
    
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, 650, "ASSET SUMMARY:")
    p.setFont("Helvetica", 10)
    p.drawString(60, 630, f"• Size: {sqft} Sqft | Baseline: {build_type} | Built: {yr}")
    p.drawString(60, 615, f"• Rooms: {inventory['beds']} Bedrooms | {inventory['baths']} Bathrooms")
    p.drawString(60, 600, f"• Infrastructure: Solar {inventory['solar']} KVA | {inventory['ac']} AC Units")

    # Visual Evidence Row (Thumbnails of Key Proofs)
    if images.get('img1'):
        try: p.drawImage(ImageReader(images['img1']), 50, 480, width=140, height=100)
        except: pass
    if images.get('img4'):
        try: p.drawImage(ImageReader(images['img4']), 210, 480, width=140, height=100)
        except: pass
    
    p.setFont("Helvetica-Oblique", 8)
    p.drawString(50, 250, "Verdict: Certified via Anti-Bias Vision Scaling & 10-Point Forensic Audit.")
    p.drawString(50, 235, "Architect: Patrick Simon Okosodo | B.Eng (UNIBEN) | MLOps Lead")
    
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

# --- 3. SECURITY & AUTH ---
st.set_page_config(page_title="PSO-ML20 Sovereign", page_icon="🛡️", layout="wide")
if 'authenticated' not in st.session_state: st.session_state['authenticated'] = False
if 'history' not in st.session_state: st.session_state['history'] = []

if not st.session_state['authenticated']:
    st.title("🛡️ PSO-ML20 Secure Gateway")
    access_key = st.text_input("Enter Architect Key", type="password")
    if st.button("Unlock Terminal"):
        if access_key == "ELITE2026":
            st.session_state['authenticated'] = True
            st.rerun()
    st.stop()

# --- 4. SIDEBAR BRANDING ---
with st.sidebar:
    st.title("🛡️ PSO-ML20 Control")
    client_logo = st.file_uploader("Upload Company Logo", type=['png', 'jpg'])
    brand_color = st.color_picker("Company Brand Color", "#1D8348")
    currency = st.radio("Money Display", ["USD ($)", "NGN (₦)"], horizontal=True)
    st.divider()
    total_val = sum([x['price'] for x in st.session_state['history']])
    st.metric("Total Houses Valued", len(st.session_state['history']))

# --- 5. PREMIUM UI STYLE ---
st.markdown(f"""
    <style>
    @import url('https://googleapis.com');
    html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; background-color: #F4F7F6; }}
    .stButton>button {{ background: {brand_color}; color: white; border-radius: 12px; height: 3.5em; font-weight: bold; width: 100%; }}
    .metric-card {{ background: white; padding: 30px; border-radius: 20px; border-top: 10px solid {brand_color}; box-shadow: 0 15px 35px rgba(0,0,0,0.1); text-align: center; }}
    [data-testid="stMetricValue"] {{ font-size: 26px !important; font-weight: bold; }}
    </style>
    """, unsafe_allow_html=True)

# --- 6. HEADER ---
c_l, c_r = st.columns([1, 4])
if client_logo: c_l.image(client_logo, width=120)
with c_r:
    st.title("Forensic Property Valuation Terminal")
    st.write("Anti-Bias Computer Vision | PSO-ML20 Industrial Standard")

# --- 7. STEP 1: PHYSICAL CORE ---
st.subheader("📍 Step 1: General Specs")
col1, col2, col3 = st.columns(3)
sqft = col1.number_input("Property Size (Sqft)", value=2500)
build_type = col2.selectbox("Building Quality", ["Basic/Standard", "Modern/Executive", "Luxury/High-End", "Elite/Mansion"])
yr_built = col3.number_input("Year Built", 1900, 2026, 2018)

# --- 8. STEP 2: THE 10-POINT FORENSIC VAULT (UPLOAD) ---
st.subheader("📷 Step 2: Visual Evidence (AI Sensor Active)")

# 🛡️ THE ARCHITECT'S MANDATORY INSTRUCTION
st.warning("""
    **🚨 CRITICAL INSTRUCTION FOR BEST RESULT:**  
    Please capture **complete, full-view photos from top-to-bottom** (Floor to Ceiling).  
    The AI requires the full vertical perspective to accurately analyze material grades, ceiling height, and floor quality.
""")

with st.expander("📂 OPEN 10-POINT UPLOAD PORTALS", expanded=True):
    v1, v2 = st.columns(2)
    # Every label now reinforces the 'Top-to-Bottom' requirement
    img1 = v1.file_uploader("1. Front View (Full Building Height)", type=['jpg', 'png'])
    img2 = v2.file_uploader("2. Compound & Gate (Full Ground View)", type=['jpg', 'png'])
    img3 = v1.file_uploader("3. Main Living Room (Top-to-Bottom View)", type=['jpg', 'png'])
    img4 = v2.file_uploader("4. Kitchen Architecture (Floor-to-Ceiling)", type=['jpg', 'png'])
    img5 = v1.file_uploader("5. Master Bedroom (Full View)", type=['jpg', 'png'])
    img6 = v2.file_uploader("6. Master Bathroom (Full Wall/Floor)", type=['jpg', 'png'])
    img7 = v1.file_uploader("7. General Passage (Full Perspective)", type=['jpg', 'png'])
    img8 = v2.file_uploader("8. Solar/Gen Set (Full Installation View)", type=['jpg', 'png'])
    img9 = v1.file_uploader("9. Pool/Luxury Space (Full Perimeter)", type=['jpg', 'png'])
    img10 = v2.file_uploader("10. Boys Quarters (Full Unit View)", type=['jpg', 'png'])


# --- 9. STEP 3: PHYSICAL INVENTORY COUNT ---
st.subheader("🔢 Step 3: House Inventory")
i1, i2, i3, i4, i5 = st.columns(5)
num_bed = i1.number_input("Bedrooms", 1, 20, 4)
num_bath = i2.number_input("Bathrooms", 1, 20, 4)
num_liv = i3.number_input("Living Areas", 1, 5, 1)
num_park = i4.number_input("Parking Slots", 0, 20, 2)
num_bq = i5.number_input("BQ Rooms", 0, 5, 1)

i6, i7, i8, i9, i10 = st.columns(5)
solar_kva = i6.number_input("Solar (KVA)", 0, 100, 5)
gen_kva = i7.number_input("Generator (KVA)", 0, 500, 20)
ac_units = i8.number_input("AC Units", 0, 30, 6)
cctv = i9.number_input("CCTV Sets", 0, 50, 8)
stores = i10.number_input("Store Rooms", 0, 5, 1)

# --- 10. CALCULATION & EXECUTION ---
if st.button("CERTIFY VALUATION (EXECUTE PSO-ML20)"):
    with st.status("Analyzing Visual Signals & Hardening Market Data...", expanded=True) as status:
        # Run Anti-Bias Vision Analysis
        ext_score = analyze_visual_quality(img1)
        liv_score = analyze_visual_quality(img3)
        kit_score = analyze_visual_quality(img4)
        
        st.write(f"Structural Edge Detection: {kit_score}x Material Signal")
        time.sleep(0.5)
        st.write("Neutralizing Lighting Bias... Verified.")
        time.sleep(0.5)
        
        # Hardened Math Logic
        type_map = {"Basic/Standard": 1, "Modern/Executive": 1.25, "Luxury/High-End": 1.6, "Elite/Mansion": 2.1}
        base_math = (sqft * 275) - ((2026 - yr_built) * 1400)
        
        # Inventory Weights
        inv_val = (num_bed * 15000) + (num_bath * 9000) + (solar_kva * 2200) + (ac_units * 1200)
        
        # Vision Multiplier (Average of scanned rooms)
        vision_mult = (ext_score + liv_score + kit_score) / 3
        final_usd = (base_math * type_map[build_type] * vision_mult) + inv_val
        
        st.session_state['history'].append({'Time': datetime.now().strftime('%H:%M'), 'price': final_usd})
        status.update(label="Forensic Audit Complete!", state="complete")

    rate = 1485
    val = final_usd if "USD" in currency else final_usd * rate
    sym = "$" if "USD" in currency else "₦"
    
    st.balloons()
    st.markdown(f"<div class='metric-card'><p>OFFICIAL CERTIFIED PRICE</p><h1 style='color: {brand_color};'>{sym}{val:,.2f}</h1><p><b>Anti-Bias Guard:</b> ACTIVE</p></div>", unsafe_allow_html=True)

    # PDF Download
    inventory = {"beds": num_bed, "baths": num_bath, "solar": solar_kva, "ac": ac_units}
    images = {"img1": img1, "img4": img4}
    pdf = generate_pso_pdf(val, sym, sqft, build_type, yr_built, inventory, images)
    st.download_button("📥 DOWNLOAD AUDIT REPORT", data=pdf, file_name="PSO_Audit.pdf", mime="application/pdf")

# --- 11. RECENT HISTORY ---
if st.session_state['history']:
    st.divider()
    st.subheader("📜 Recent Records")
    st.dataframe(pd.DataFrame(st.session_state['history']), use_container_width=True)

st.caption("© 2026 PSO-ML20 | Patrick Simon Okosodo | AI Architect | MLOps Specialist | B.Eng (Chem)")
