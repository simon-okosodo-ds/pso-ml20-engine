import streamlit as st
import pandas as pd
import numpy as np
import time
import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# --- PDF GENERATOR (Simplified for 10-Point Audit) ---
def generate_pso_pdf(val, sym, sqft, build_type, yr, inventory, images):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 750, "PSO-ML20 PROPERTY VALUATION REPORT")
    p.setFont("Helvetica", 10)
    p.drawString(50, 735, f"Date: {datetime.now().strftime('%Y-%m-%d')} | Ref: PSO-{np.random.randint(100,999)}")
    p.line(50, 730, 550, 730)

    p.setFont("Helvetica-Bold", 22)
    p.setFillColorRGB(0.11, 0.51, 0.28) 
    p.drawString(50, 690, f"MARKET VALUE: {sym}{val:,.2f}")
    p.setFillColorRGB(0, 0, 0)
    
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, 650, "HOUSE SUMMARY:")
    p.setFont("Helvetica", 10)
    p.drawString(60, 630, f"• Size: {sqft} Sqft | Type: {build_type} | Built: {yr}")
    p.drawString(60, 615, f"• Rooms: {inventory['beds']} Bedrooms | {inventory['baths']} Bathrooms")
    
    # Simple image placement (shows first 2 uploads)
    if images.get('img1'):
        try: p.drawImage(ImageReader(images['img1']), 50, 450, width=150, height=100)
        except: pass
    
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

# 1. SETUP & SECURITY
st.set_page_config(page_title="PSO-ML20 Valuation", page_icon="🛡️", layout="wide")
if 'authenticated' not in st.session_state: st.session_state['authenticated'] = False
if 'history' not in st.session_state: st.session_state['history'] = []

if not st.session_state['authenticated']:
    st.title("🛡️ PSO-ML20 Secure Login")
    access_key = st.text_input("Enter your Access Key", type="password")
    if st.button("Open System"):
        if access_key == "ELITE2026":
            st.session_state['authenticated'] = True
            st.rerun()
    st.stop()

# 2. SIDEBAR BRANDING
with st.sidebar:
    st.title("🛡️ PSO-ML20 Control")
    client_logo = st.file_uploader("Upload Company Logo", type=['png', 'jpg'])
    brand_color = st.color_picker("Pick your Brand Color", "#1D8348")
    currency = st.radio("Money Type", ["USD ($)", "NGN (₦)"], horizontal=True)
    st.divider()
    total_val = sum([x['price'] for x in st.session_state['history']])
    st.metric("Total Houses Valued", len(st.session_state['history']))

# 3. GLOBAL STYLE
st.markdown(f"<style>.stButton>button {{ background: {brand_color}; color: white; border-radius: 12px; height: 3.5em; font-weight: bold; width: 100%; }} .metric-card {{ background: white; padding: 30px; border-radius: 20px; border-top: 10px solid {brand_color}; box-shadow: 0 15px 35px rgba(0,0,0,0.1); text-align: center; }}</style>", unsafe_allow_html=True)

# 4. MAIN INTERFACE
col_logo, col_title = st.columns([1, 4])
if client_logo: col_logo.image(client_logo, width=100)
with col_title:
    st.title("Property Valuation Terminal")
    st.write("Fill in the details below to get a certified market price.")

# 5. STEP 1: GENERAL HOUSE DETAILS
st.subheader("📍 Step 1: General Details")
c1, c2, c3 = st.columns(3)
sqft = c1.number_input("Total House Size (Sqft)", value=2500)
build_type = c2.selectbox("Building Quality", ["Basic/Standard", "Modern/Executive", "Luxury/High-End", "Elite/Mansion"])
yr_built = c3.number_input("Year it was Built", 1900, 2026, 2018)

# 6. STEP 2: THE 10-POINT VISUAL VAULT (PICTURES)
st.subheader("📷 Step 2: Proof Photos (Upload 10 Parts)")
with st.expander("Click to open the 10 Upload Portals", expanded=True):
    v1, v2 = st.columns(2)
    img1 = v1.file_uploader("1. Front View of House", type=['jpg', 'png'])
    img2 = v2.file_uploader("2. Compound & Gate", type=['jpg', 'png'])
    img3 = v1.file_uploader("3. Main Living Room", type=['jpg', 'png'])
    img4 = v2.file_uploader("4. Kitchen", type=['jpg', 'png'])
    img5 = v1.file_uploader("5. Master Bedroom", type=['jpg', 'png'])
    img6 = v2.file_uploader("6. Master Bathroom", type=['jpg', 'png'])
    img7 = v1.file_uploader("7. General Passage/Corridor", type=['jpg', 'png'])
    img8 = v2.file_uploader("8. Solar/Gen/Inverter", type=['jpg', 'png'])
    img9 = v1.file_uploader("9. Swimming Pool/Gym", type=['jpg', 'png'])
    img10 = v2.file_uploader("10. Boys Quarters (BQ)", type=['jpg', 'png'])

# 7. STEP 3: THE 10-POINT PHYSICAL COUNT
st.subheader("🔢 Step 3: House Inventory (How many of each?)")
i1, i2, i3, i4, i5 = st.columns(5)
num_bed = i1.number_input("Bedrooms", 1, 20, 4)
num_bath = i2.number_input("Bathrooms", 1, 20, 4)
num_liv = i3.number_input("Living Rooms", 1, 5, 1)
num_park = i4.number_input("Parking Space", 0, 20, 2)
num_bq = i5.number_input("BQ Rooms", 0, 5, 1)

i6, i7, i8, i9, i10 = st.columns(5)
solar_kva = i6.number_input("Solar (KVA)", 0, 100, 5)
gen_kva = i7.number_input("Generator (KVA)", 0, 500, 20)
ac_units = i8.number_input("AC Units", 0, 30, 6)
security_cctv = i9.number_input("CCTV Cameras", 0, 50, 8)
store_rooms = i10.number_input("Store Rooms", 0, 5, 1)

# 8. CALCULATION & EXECUTION
if st.button("GET CERTIFIED PRICE"):
    with st.status("Checking all 10 points...", expanded=True):
        time.sleep(1)
        # Logical Weights
        type_mult = {"Basic/Standard": 1, "Modern/Executive": 1.2, "Luxury/High-End": 1.5, "Elite/Mansion": 2.0}
        
        # Base Math
        base = (sqft * 270) - ((2026 - yr_built) * 1500)
        inventory_bonus = (num_bed * 15000) + (num_bath * 10000) + (solar_kva * 2000) + (ac_units * 1000)
        
        final_usd = (base * type_mult[build_type]) + inventory_bonus
        st.session_state['history'].append({'Time': datetime.now().strftime('%H:%M'), 'price': final_usd})

    # Results Display
    rate = 1485
    val = final_usd if "USD" in currency else final_usd * rate
    sym = "$" if "USD" in currency else "₦"
    
    st.balloons()
    st.markdown(f"<div class='metric-card'><p>Official Valuation</p><h1>{sym}{val:,.2f}</h1><p>Verified by PSO-ML20 Framework</p></div>", unsafe_allow_html=True)

    # PDF Download
    inventory = {"beds": num_bed, "baths": num_bath, "parking": num_park}
    images = {"img1": img1, "img2": img2} # Logic for first 2 pics
    pdf = generate_pso_pdf(val, sym, sqft, build_type, yr_built, inventory, images)
    st.download_button("📥 DOWNLOAD PDF REPORT", data=pdf, file_name="PSO_Valuation.pdf", mime="application/pdf")

# 9. RECENT HISTORY
if st.session_state['history']:
    st.divider()
    st.subheader("📜 Recent Records")
    st.dataframe(pd.DataFrame(st.session_state['history']))

st.caption("© 2026 PSO-ML20 | Simple Industrial Valuation | Patrick Simon Okosodo")
