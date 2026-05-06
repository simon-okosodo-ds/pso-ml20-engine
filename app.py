import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# --- PDF GENERATOR ENGINE (THE CERTIFICATE) ---
def generate_pso_pdf(val, sym, sqft, grade, yr, inventory, tech, images):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 750, "PSO-ML20 INDUSTRIAL FORENSIC CERTIFICATE")
    p.setFont("Helvetica", 10)
    p.drawString(50, 735, f"Issued: {datetime.now().strftime('%Y-%m-%d')} | Ref: PSO-{np.random.randint(100,999)}")
    p.line(50, 730, 550, 730)

    p.setFont("Helvetica-Bold", 24)
    p.setFillColorRGB(0.11, 0.51, 0.28) 
    p.drawString(50, 690, f"CERTIFIED VALUE: {sym}{val:,.2f}")
    p.setFillColorRGB(0, 0, 0)
    
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, 650, "PHYSICAL ARCHITECTURE AUDIT:")
    p.setFont("Helvetica", 10)
    p.drawString(60, 630, f"• Size: {sqft} Sqft | Grade: {grade}/13 | Built: {yr}")
    p.drawString(60, 615, f"• Inventory: {inventory['beds']} Beds | {inventory['baths']} Baths | {inventory['parking']} Parking")
    p.drawString(60, 600, f"• Infrastructure: Solar {tech['solar']} KVA | Security: {tech['sec']}")

    # Visual Evidence Grid
    y_pos = 450
    if images.get('ext'):
        p.drawImage(ImageReader(images['ext']), 50, y_pos, width=140, height=90)
        p.drawString(50, y_pos-10, "Exterior Evidence")
    if images.get('kit'):
        p.drawImage(ImageReader(images['kit']), 210, y_pos, width=140, height=90)
        p.drawString(210, y_pos-10, "Interior Evidence")
    
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

# 1. AUTHENTICATION & CONFIG
st.set_page_config(page_title="PSO-ML20 Enterprise", page_icon="🛡️", layout="wide")
if 'history' not in st.session_state: st.session_state['history'] = []
if 'authenticated' not in st.session_state: st.session_state['authenticated'] = False

# 2. LOGIN GATEWAY
if not st.session_state['authenticated']:
    st.markdown("<h1 style='text-align: center;'>🛡️ PSO-ML20 SECURE GATEWAY</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        access_key = st.text_input("ACCESS KEY", type="password")
        if st.button("AUTHORIZE"):
            if access_key == "ELITE2026":
                st.session_state['authenticated'] = True
                st.rerun()
    st.stop()

# 3. SIDEBAR (Branding & ROI)
with st.sidebar:
    st.title("🛡️ PSO-ML20 Control")
    client_logo = st.file_uploader("Company Logo", type=['png', 'jpg'])
    brand_color = st.color_picker("Brand Color", "#1D8348")
    currency = st.radio("Currency", ["USD ($)", "NGN (₦)"], horizontal=True)
    st.divider()
    total_val = sum([x['price'] for x in st.session_state['history']])
    st.metric("Assets Valued", len(st.session_state['history']))
    st.metric("Session ROI", f"${total_val:,.0f}")

# 4. CUSTOM STYLING
st.markdown(f"<style>.stButton>button {{ background: {brand_color}; color: white; border-radius: 12px; height: 3.5em; font-weight: bold; width: 100%; }} .metric-card {{ background: white; padding: 30px; border-radius: 20px; border-top: 10px solid {brand_color}; box-shadow: 0 15px 35px rgba(0,0,0,0.1); text-align: center; }} [data-testid='stMetricValue'] {{ font-size: 26px !important; }}</style>", unsafe_allow_html=True)

# 5. HEADER
col_l, col_r = st.columns([1,4])
if client_logo: col_l.image(client_logo, width=100)
col_r.title("Industrial Valuation Terminal")

# 6. MANUAL INPUTS & DROPDOWNS
st.subheader("📍 Forensic Asset Ingestion")
c1, c2, c3 = st.columns(3)
sqft = c1.number_input("Property Area (Sqft)", value=2500)
grade = c2.slider("Build Grade (1-13)", 1, 13, 7)
yr_built = c3.number_input("Year Built", 1900, 2026, 2018)

# 7. DROPDOWN SELECTORS (MANUAL CLICKING)
st.subheader("🛠️ Detailed Specifications (Manual Selection)")
d1, d2 = st.columns(2)
kitchen_finish = d1.selectbox("Kitchen Finishing Grade", ["Standard", "Imported Marble", "Italian Quartz", "High-Gloss Luxury"])
pool_type = d2.selectbox("Aquatic Assets", ["None", "Surface Level", "Infinity Edge", "Olympic Standard"])

# 8. THE 10-POINT VISUAL VAULT (UPLOAD)
st.subheader("📷 Visual Evidence Vault")
with st.expander("📂 Click to Upload Proof Photos", expanded=False):
    v1, v2 = st.columns(2)
    ext_img = v1.file_uploader("1. Building Face", type=['jpg', 'png'])
    kit_img = v2.file_uploader("2. Kitchen Detail", type=['jpg', 'png'])
    pow_img = v1.file_uploader("3. Energy/Inverter Set", type=['jpg', 'png'])
    bq_img = v2.file_uploader("4. Staff Quarters (BQ)", type=['jpg', 'png'])

# 9. COUNTERS & TECH
st.subheader("🔢 Physical Inventory & Tech")
i1, i2, i3, i4 = st.columns(4)
num_bed = i1.number_input("Bedrooms", 1, 20, 4)
num_bath = i2.number_input("Bathrooms", 1, 20, 4)
num_parking = i3.number_input("Parking", 0, 20, 2)
solar_kva = i4.number_input("Solar (KVA)", 0, 100, 5)

sec_tier = st.select_slider("Security Architecture", options=["Basic", "Electric Fence", "CCTV Integrated", "Armed Gated"])

# 11. EXECUTION
if st.button("CERTIFY & EXECUTE PSO-ML20"):
    with st.status("Applying PSO-ML20 Hardening...", expanded=True):
        time.sleep(1)
        # Advanced Logic
        k_mult = {"Standard": 1, "Imported Marble": 1.1, "Italian Quartz": 1.2, "High-Gloss Luxury": 1.35}
        p_bonus = {"None": 0, "Surface Level": 25000, "Infinity Edge": 60000, "Olympic Standard": 150000}
        
        base = (sqft * 272) + (grade * 52000) - ((2026-yr_built) * 1800)
        final_usd = (base * k_mult[kitchen_finish]) + p_bonus[pool_type] + (solar_kva * 2000)
        
        st.session_state['history'].append({'Time': datetime.now().strftime('%H:%M'), 'price': final_usd})

    rate = 1485
    val = final_usd if "USD" in currency else final_usd * rate
    sym = "$" if "USD" in currency else "₦"
    
    st.balloons()
    st.markdown(f"<div class='metric-card'><p>Official Certified Valuation</p><h1>{sym}{val:,.2f}</h1></div>", unsafe_allow_html=True)

    # RE-SYNC PDF DATA
    inventory = {"beds": num_bed, "baths": num_bath, "parking": num_parking}
    tech = {"solar": solar_kva, "sec": sec_tier}
    images = {"ext": ext_img, "kit": kit_img}
    
    pdf = generate_pso_pdf(val, sym, sqft, grade, yr_built, inventory, tech, images)
    st.download_button("📥 DOWNLOAD AUDIT REPORT", data=pdf, file_name="PSO_Certificate.pdf", mime="application/pdf")

# 12. HISTORY
if st.session_state['history']:
    st.divider()
    st.subheader("📜 Recent Valuation History")
    st.dataframe(pd.DataFrame(st.session_state['history']))

st.caption("© 2026 PSO-ML20 | Industrial Data Science Framework | Patrick Simon Okosodo")
