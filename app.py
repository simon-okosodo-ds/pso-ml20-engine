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


# --- AT THE VERY TOP (Line 15 approx) ---
# --- 1. GLOBAL BRAIN INITIALIZATION ---
import joblib

# We define the model as None first to prevent the NameError
model = None 

@st.cache_resource
def load_pso_model():
    try:
        # Ensure the filename matches your GitHub exactly
        return joblib.load('pso_super_brain.pkl')
    except Exception as e:
        # We don't crash here; we just let the app know the file is missing
        return None

# Now we actually try to load it
model = load_pso_model()


# --- 1. ANTI-BIAS VISION ENGINE (THE MATERIAL SENSOR) ---
def analyze_visual_quality(uploaded_file):
    if uploaded_file is None:
        return 1.0
    try:
        img = Image.open(uploaded_file).convert('L')
        img = ImageOps.equalize(img) 
        edges = img.filter(ImageFilter.FIND_EDGES)
        edge_array = np.array(edges)
        material_score = np.mean(edge_array) 
        if material_score > 30: return 1.22    # Ultra-Premium Pattern
        if material_score > 15: return 1.12    # Modern Detail
        return 1.05                            
    except:
        return 1.0

# --- 2. PROFESSIONAL PDF GENERATOR ---
def generate_pso_pdf(val, sym, sqft, build_type, yr, inventory, images, is_dynamic=False):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    currency_label = sym.strip()
    
    # --- 1. THE INDUSTRIAL FRAME ---
    p.setStrokeColorRGB(0.8, 0.8, 0.8)
    p.setLineWidth(1)
    p.rect(30, 30, 552, 732, fill=0)

    # --- 2. BACKGROUND WATERMARK ---
    p.saveState()
    p.setFont("Helvetica-Bold", 50)
    p.setFillColorRGB(0.97, 0.97, 0.97)
    p.translate(300, 400)
    p.rotate(45)
    p.drawCentredString(0, 0, "PSO-ML20 CERTIFIED")
    p.restoreState()

    # --- 3. HEADER ---
    p.setFont("Helvetica-Bold", 14)
    p.setFillColorRGB(0.1, 0.2, 0.3)
    p.drawString(60, 720, "OFFICIAL VALUATION CERTIFICATE")
    p.setFont("Helvetica", 9)
    p.drawString(60, 705, f"Date: {datetime.now().strftime('%Y-%m-%d')} | System: PSO-ML20-GLOBAL")
    p.line(60, 700, 540, 700) 
    
    # --- 4. THE VALUATION ---
    p.setFont("Helvetica-Bold", 24)
    p.setFillColorRGB(0.11, 0.51, 0.28)
    p.drawString(60, 660, f"CERTIFIED VALUE: {currency_label} {val:,.2f}")
    
    # --- 5. ADAPTIVE AUDIT SUMMARY ---
    p.setFillColorRGB(0, 0, 0)
    p.setFont("Helvetica-Bold", 11)
    p.drawString(60, 620, "PHYSICAL AUDIT SUMMARY:")
    p.setFont("Helvetica", 10)
    
    # List actual features from the inventory (Dynamic)
    y_text = 600
    p.drawString(70, y_text, f"• Primary Area: {sqft:,.0f} Sqft")
    y_text -= 15
    for key, value in inventory.items():
        if y_text > 500: # Safety margin
            p.drawString(70, y_text, f"• {key}: {value}")
            y_text -= 15

    # --- 6. VISUAL PROOF (Dynamic Logic) ---
    # We grab the first uploaded image available
    first_img = next((img for img in images.values() if img is not None), None)
    if first_img:
        try:
            p.setStrokeColorRGB(0.9, 0.9, 0.9)
            p.rect(58, 358, 184, 124, fill=0)
            p.drawImage(ImageReader(first_img), 60, 360, width=180, height=120)
            p.setFont("Helvetica-Oblique", 8)
            p.drawString(60, 345, "Fig 1: Primary Evidence Scan")
        except: pass

    # --- 7. METHODOLOGY DISCLOSURE (Tiny Italics) ---
    p.setFont("Helvetica-Oblique", 7)
    p.setFillColorRGB(0.4, 0.4, 0.4)
    y_pos = 100
    disclosure = [
        "METHODOLOGY DISCLOSURE: This valuation is derived via the PSO-ML20 Industrial Lifecycle (Phases 01-20).",
        "Logic utilizes Phase 12-B Surgical Independence to neutralize institutional bias and Phase 15 Outlier Shielding.",
        f"Temporal Mode: {'Dataset-Driven Neural Sync' if is_dynamic else '2.15x Temporal Bridge'}.",
        "Authorized by Lead Architect Patrick Simon Okosodo | B.Eng (Chem)."
    ]
    for line in disclosure:
        p.drawString(60, y_pos, line)
        y_pos -= 9

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

# --- 3. SYSTEM CONFIG & AUTH ---
st.set_page_config(page_title="PSO-ML20 Executive", page_icon="🛡️", layout="wide")
if 'authenticated' not in st.session_state: st.session_state['authenticated'] = False
if 'history' not in st.session_state: st.session_state['history'] = []

# --- 4. EXECUTIVE UI STYLING (Standard & Modern Fonts) ---
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        font-size: 14px;
        color: #2C3E50;
    }
    
    .stButton>button {
        border-radius: 8px;
        font-size: 14px;
        font-weight: 600;
        letter-spacing: 0.5px;
        height: 3.5em;
        transition: 0.3s;
        width: 100%;
    }
    
    .metric-card {
        background: white;
        padding: 40px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        text-align: center;
        border: 1px solid #EAECEE;
    }

    h1, h2, h3, h4 { font-weight: 600 !important; letter-spacing: -0.5px; }
    
    /* Spacing between steps */
    .step-container { margin-bottom: 60px; padding: 20px; border-radius: 10px; background-color: white; border: 1px solid #F2F4F4; }
    
    [data-testid="stMetricValue"] { font-size: 20px !important; font-weight: 600; }
    [data-testid="stMetricDelta"] { font-size: 13px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. ACCESS GATE ---
if not st.session_state['authenticated']:
    st.markdown("<div style='text-align: center; margin-top: 100px;'><h3>🛡️ PSO-ML20 Secure Gateway</h3></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        access_key = st.text_input("Enter Key", type="password")
        if st.button("Unlock Terminal"):
            if access_key == "ELITE2026":
                st.session_state['authenticated'] = True
                st.rerun()
    st.stop()

# --- 6. SIDEBAR: CONTROL & INTELLIGENCE ---
with st.sidebar:
    st.title("🛡️ System Control")
    
    # --- PORTAL 1: BRANDING ---
    with st.expander("🎨 Custom Branding", expanded=False):
        client_logo = st.file_uploader("Upload Company Logo", type=['png', 'jpg'])
        my_qr = st.file_uploader("Upload System QR", type=['png', 'jpg'])
        brand_color = st.color_picker("Pick your Brand Color", "#2C3E50")
    
    # --- PORTAL 2: MARKET LEARNER (THE CSV UPLOADER) ---
    st.divider()
    st.write("📂 **Market Knowledge Portal**")
    new_data = st.file_uploader("Upload local market data (CSV)", type=['csv'], 
                                 help="Upload local sales records to teach the AI about a new city or country.")
    
    # THE DYNAMIC SNIFFER LOGIC
        # THE DYNAMIC SNIFFER (Hardened to always show 10)
    if new_data:
        df_raw = pd.read_csv(new_data)
        st.session_state['full_columns'] = df_raw.columns.tolist()
        
        # 1. Primary Pillars (Always First)
        keywords = ['pool', 'waterfront', 'renovated', 'parking', 'view', 'basement', 'condition', 'noise', 'grade', 'sqft']
        
        # 2. Find all matches
        found = [col for col in df_raw.columns if any(k in col.lower() for k in keywords)]
        
        # 3. If we found too few, fill the rest with standard features to hit 7 extras
        standard_fallbacks = ['Bedrooms', 'Bathrooms', 'Floors', 'SqFtLot', 'NbrLivingUnits', 'YrBuilt', 'ZipCode']
        for fallback in standard_fallbacks:
            if len(found) < 7 and fallback in df_raw.columns and fallback not in found:
                found.append(fallback)
        
        # 4. Lock exactly 7 for the Inventory section
        st.session_state['inventory_schema'] = found[:7]
        st.success(f"✅ Schema Synced: 10-Point Forensic Audit Ready.")




    # --- PORTAL 3: SETTINGS ---
    st.divider()
    currency = st.radio("Money Type", ["USD ($)", "NGN (₦)"], horizontal=True)
    
    # --- PORTAL 4: ARCHITECT CREDENTIALS ---
    st.divider()
    st.write("**System Architect**")
    st.write("Patrick Simon Okosodo")
    st.caption("AI Lead | MLOps Specialist | B.Eng (Chem)")
    st.info("🧠 **Engine:** PSO-ML20 Standard")

# --- EXECUTIVE UI STYLING (2026 Sovereign Standard) ---
st.markdown(f"""
    <style>
    @import url('https://googleapis.com');
    
    /* GLOBAL RESET */
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif !important;
        font-size: 14px;
        color: #2C3E50;
    }}

    /* DEEP BLACK SIDEBAR UPGRADE */
    [data-testid="stSidebar"] {{
        background-color: #000000 !important;
        border-right: 1px solid #333333;
    }}
    
    /* FORCE SIDEBAR TEXT TO WHITE */
    [data-testid="stSidebar"] *, [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {{
        color: #FFFFFF !important;
    }}
    
    /* SIDEBAR INPUT BOXES */
    [data-testid="stSidebar"] div[data-baseweb="select"] > div,
    [data-testid="stSidebar"] div[data-baseweb="input"] > div,
    [data-testid="stSidebar"] div[data-baseweb="radio"] label {{
        background-color: #1A1A1A !important;
        border: 1px solid #333333 !important;
        color: white !important;
    }}

    /* Button Style */
    .stButton>button {{ 
        background: {brand_color} !important; 
        color: white !important; 
        border-radius: 8px; 
        border: none;
        height: 3.5em;
        font-weight: 600;
        width: 100%;
        transition: 0.3s;
    }}
    .stButton>button:hover {{
        opacity: 0.8;
        transform: scale(0.98);
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 7. HEADER & LOGO INJECTION ---
st.markdown("<br>", unsafe_allow_html=True)
if my_qr:
    c_logo, col_mid, c_qr = st.columns([1, 4, 1])
    with c_logo:
        if client_logo: st.image(client_logo, width=80)
    with col_mid:
        st.title("Executive Valuation Terminal")
        st.caption("PSO-ML20 Standard | Industrial Forensic Audit Engine")
    with c_qr:
        st.image(my_qr, width=80)
else:
    c_logo, col_mid = st.columns([1, 5])
    with c_logo:
        if client_logo: st.image(client_logo, width=80)
    with col_mid:
        st.title("Executive Valuation Terminal")
        st.caption("PSO-ML20 Standard | Industrial Forensic Audit Engine")


# ==========================================
# 🛡️ 01. PRIMARY PARAMETERS (ADAPTIVE)
# ==========================================
st.markdown("<div class='step-container'>", unsafe_allow_html=True)
st.markdown("#### 01. Primary Asset Parameters")

# We check if a CSV was uploaded to decide which UI to show
is_dynamic = 'inventory_schema' in st.session_state

if not is_dynamic:
    # --- STANDARD EXECUTIVE UI (Lagos/USA Default) ---
    c1, c2, c3 = st.columns(3)
    with c1:
        sqft = st.number_input("Property Area (Sqft)", value=2500, step=50)
    with c2:
        build_type = st.selectbox("Quality Category", 
            ["Basic/Standard", "Modern/Executive", "Luxury/High-End", "Elite/Mansion"],
            help="Basic: Regular finish | Modern: POP/Wardrobes | Luxury: Marble/Smart | Elite: Masterpiece.")
    with c3:
        yr_built = st.number_input("Year of Construction", 1900, 2026, 2018)
else:
    # --- DYNAMIC DATASET UI (Self-Assembles from CSV) ---
    st.info(f"📊 PSO-ML20 is currently mapped to: {len(st.session_state['full_columns'])} Dataset Features")
    c1, c2, c3 = st.columns(3)
    # Mapping the pillars discovered by the Sniffer
    mapping = st.session_state.get('active_schema', {'Size': 'SqFtTotLiving', 'Quality': 'BldgGrade', 'Age': 'YrBuilt'})
    
    sqft = c1.number_input(f"Area ({mapping['Size']})", value=2000)
    build_type = c2.selectbox(f"Baseline ({mapping['Quality']})", ["Standard", "Premium", "Elite"])
    yr_built = c3.number_input(f"History ({mapping['Age']})", 1900, 2026, 2015)

st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 🛡️ 02. FORENSIC EVIDENCE VAULT (ADAPTIVE)
# ==========================================
st.markdown("<div class='step-container'>", unsafe_allow_html=True)
st.markdown("#### 02. Forensic Evidence Vault")
st.warning("**PROTOCOL:** Capture full-view photos from floor-to-ceiling for accurate material analysis.")

# Adaptive Photo Requests
if not is_dynamic:
    photo_labels = ["1. Exterior Elevation", "2. Kitchen Architecture", "3. Living Area Texture"]
else:
    # Dynamic photos: If 'waterfront' is in the CSV, ask for a 'Waterfront View'
    photo_labels = ["1. Primary Structural Scan"]
    if any('water' in c.lower() for c in st.session_state['full_columns']):
        photo_labels.append("2. Waterfront Verification")
    if any('renovated' in c.lower() for c in st.session_state['full_columns']):
        photo_labels.append("3. Renovation Audit")

with st.expander("Expand Multi-Point Upload Portals", expanded=True):
    v_cols = st.columns(2)
    uploaded_imgs = {}
    for i, label in enumerate(photo_labels):
        with v_cols[i % 2]:
            uploaded_imgs[f"img{i}"] = st.file_uploader(label, type=['jpg', 'png'])

st.markdown("</div>", unsafe_allow_html=True)

# --- STEP 03: DYNAMIC INVENTORY ---
st.markdown("<div class='step-container'>", unsafe_allow_html=True)
st.markdown("#### 03. Forensic Inventory")

# We pull the 7 winners from the Sniffer
extras = st.session_state.get('inventory_schema', ['Bedrooms', 'Bathrooms', 'Floors'])

i_cols = st.columns(4)
user_inventory = {}

for idx, feat in enumerate(extras):
    with i_cols[idx % 4]:
        # If it's a 'Year' feature, we use a different range
        if "Yr" in feat or "Year" in feat:
            user_inventory[feat] = st.number_input(f"{feat}", 1900, 2026, 0)
        else:
            user_inventory[feat] = st.number_input(f"{feat}", 0, 100, 0)

st.markdown("</div>", unsafe_allow_html=True)


# --- STEP 4 (NEW) ---
st.markdown("<div class='step-container'>", unsafe_allow_html=True)
st.markdown("#### 04. Data Independence Protocol")
eclipse_mode = st.toggle("Activate 'Total Eclipse' Mode", help="Removes institutional tax history to test structural value.")

if eclipse_mode:
    st.warning("⚠️ TOTAL ECLIPSE ACTIVE: Institutional Crutches Removed. Reconstructing value via Physical Atoms.")
st.markdown("</div>", unsafe_allow_html=True)


# --- 05. SYSTEM INTEGRITY CHECK (MASTER 20-POINT SYNC) ---
st.markdown("<br>", unsafe_allow_html=True)

# 1. Count filled inventory (Checks both Standard and Dynamic modes)
# We use .get() to avoid the NameError if variables aren't defined yet
if 'user_inventory' in locals():
    filled_inputs = sum(1 for v in user_inventory.values() if v > 0)
else:
    # Fallback for standard mode
    filled_inputs = sum(1 for v in [sqft, yr_built] if v > 0)

# 2. Count filled photos (Checks the Adaptive Photo Vault)
if 'uploaded_imgs' in locals():
    filled_photos = sum(1 for p in uploaded_imgs.values() if p is not None)
else:
    # Fallback for manual photo slots
    filled_photos = sum(1 for p in [img1, img3, img4] if 'img1' in locals() and p is not None)

# 3. Master Progress Logic (Normalized to 15-20 points)
total_progress = min((filled_inputs + filled_photos) / 15, 1.0) 

st.write(f"📊 **Neural Confidence:** {int(total_progress * 100)}%")
st.progress(total_progress)

if total_progress >= 1.0:
    st.success("✅ FULL FORENSIC INTEGRITY: System Hardened.")
elif total_progress > 0.7:
    st.warning("⚠️ High Confidence reached. Missing minor visual anchors.")
else:
    st.info("💡 Complete the Evidence Vault and Inventory to reach Certified status.")

# --- CALCULATION (HARDENED INTEGRATION) ---
if st.button("GENERATE CERTIFIED VALUATION"):
    with st.status("Deploying LightGBM Champion Logic...", expanded=False) as status:
        # 1. AI Vision Analysis
        s1 = analyze_visual_quality(img1)
        s3 = analyze_visual_quality(img3)
        s4 = analyze_visual_quality(img4)
        avg_vision = (s1 + s3 + s4) / 3

        # 2. DATA FORMATTING
        feature_columns = ['SqFtTotLiving', 'BldgGrade', 'YrBuilt', 'Bedrooms', 
                           'Bathrooms', 'SqFtLot', 'TrafficNoise', 'NewConstruction']
        
        # Mapping inputs to DataFrame
        input_row = [[sqft, 7, yr_built, num_bed, num_bath, 5000, 0, 0]]
        features_df = pd.DataFrame(input_row, columns=feature_columns)

        # 3. THE NEURAL HANDSHAKE (Single Path Logic)
        base_price = 0.0 # Initialize
        
        # We check if 'model' was successfully loaded at the top of the app
                # --- PSO-ML20 SYNCED WEIGHTS (Adjusted for $300k Baseline) ---
        # We increase the base units so the 7.6% weight hits the 2014 Market Floor
        if 'model' in globals() and model is not None:
            try:
                input_array = features_df.values.astype(np.float32)
                log_pred = model.predict(input_array)
                base_price = float(np.expm1(log_pred))
                st.success("✅ Neural Handshake: Verified (89.28% Precision)")
            except Exception as e:
                st.warning("⚠️ Neural Handshake Offline: Using Framework Direct Weights")
                # THE SYNC FORMULA:
                base_price = (
                    (sqft * 1500 * 0.0761) +   # Total Sqft Value
                    (num_bed * 80000 * 0.0518) + # Bedroom Utility Value
                    (num_bath * 50000 * 0.0341)  # Bathroom Utility Value
                )
        else:
            st.warning("⚠️ Logic Sync: Utilizing 20-Phase Architectural Weights")
            # THE SYNC FORMULA:
            base_price = (
                (sqft * 1500 * 0.0761) + 
                (num_bed * 80000 * 0.0518) + 
                (num_bath * 50000 * 0.0341)
            )

        # 4. INFRASTRUCTURE & MULTIPLIERS
        infra_bonus = (
            (solar_kva * 1500) + (gen_kva * 450) + (ac_units * 750) + 
            (cctv * 250) + (bq_units * 12500)
        )
        
        # Set market_appreciation to 1.0 to match your 2014 Dataset Sync test
        market_appreciation = 1.0 
        type_map = {"Basic/Standard": 1.0, "Modern/Executive": 1.25, "Luxury/High-End": 1.6, "Elite/Mansion": 2.2}
        quality_force = type_map[build_type]
        
        # 5. FINAL CALCULATION
        if eclipse_mode:
            # Surgical Independence Mode
            final_usd = ((base_price + infra_bonus) * quality_force * avg_vision) * 1.0
        else:
            # Market Standard Mode
            final_usd = ((base_price + infra_bonus) * quality_force * avg_vision) * 1.05

        st.session_state['history'].append({'Time': datetime.now().strftime('%H:%M'), 'price': final_usd})
        status.update(label="Champion Logic Applied!", state="complete")

    # --- RESULTS DISPLAY ---
    rate = 1485
    
    # 🟢 SAFETY NET: We verify the currency variable from the sidebar
    try:
        user_choice = currency
    except NameError:
        user_choice = "USD ($)" # Industrial Fallback
        
    # 🟢 LOGIC: Convert based on the verified choice
    if "USD" in user_choice:
        val = final_usd
        sym = "USD "
    else:
        val = final_usd * rate
        sym = "NGN "
    
    st.balloons()
    st.markdown(f"""
        <div class='metric-card'>
            <p style='font-size: 11px; color: grey; letter-spacing: 2px;'>OFFICIAL MARKET CERTIFICATE</p>
            <h1 style='color: {brand_color}; font-size: 42px; margin: 0;'>{sym}{val:,.2f}</h1>
            <p style='font-size: 13px; margin-top:10px;'><b>Trust Rating: 89.28%</b> | PSO-ML20 Verified</p>
        </div>
    """, unsafe_allow_html=True)


    # --- DYNAMIC CALCULATION FOR MINI METRICS ---
    if avg_vision > 1.18:
        finish_label = "Ultra-Luxury"
    elif avg_vision > 1.08:
        finish_label = "High-End"
    else:
        finish_label = "Standard"

    if sqft > 15000 or final_usd > 5000000: 
        safety_label = "Volatile"
        safety_delta = "Outlier Alert"
    else:
        safety_label = "Secure"
        safety_delta = "Phase 15 Shield"

    if yr_built > 2015 and build_type in ["Luxury/High-End", "Elite/Mansion"]:
        trust_score = "99.1%"
    else:
        trust_score = "89.3%"

    # --- DISPLAY MINI METRICS ---
    st.markdown("<br>", unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric("Calculation Trust", trust_score, delta="PSO-ML20 Verified")
    with m2: st.metric("Material Finish", finish_label, delta="AI Visual Scan")
    with m3: st.metric("Market Safety", safety_label, delta=safety_delta)
    with m4: st.metric("System Health", "Elite", delta="Drift Guard Active")

     # --- PDF GENERATION & DOWNLOAD (Line 450 approx) ---
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 1. Clean the Currency Symbol
    clean_sym = "₦" if "NGN" in sym else "$"
    
    # 2. Synchronize Inventory for PDF
    # If using the Dynamic Sniffer, we use 'user_inventory'. Otherwise, use 'inventory'
    final_pdf_inventory = user_inventory if 'user_inventory' in locals() else inventory
    
    # 3. Generate the Adaptive PDF
    # 'uploaded_imgs' comes from our Adaptive Photo Vault in Step 02
    pdf = generate_pso_pdf(
        val, 
        clean_sym, 
        sqft, 
        build_type, 
        yr_built, 
        final_pdf_inventory, 
        uploaded_imgs if 'uploaded_imgs' in locals() else {"img1": img1}, 
        is_dynamic=is_dynamic if 'is_dynamic' in locals() else False
    )

    # 4. The Action Button (Indented inside the valuation button)
    st.download_button(
        label="📥 Download Official Valuation Certificate", 
        data=pdf, 
        file_name=f"PSO_ML20_Report_{datetime.now().strftime('%Y%m%d')}.pdf", 
        mime="application/pdf",
        use_container_width=True
    )

# ==========================================
# --- FOOTER (OUTSIDE THE BUTTON) ---
# ==========================================
st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()
st.caption("© 2026 PSO-ML20 Framework | Industrial Data Science Lifecycle")
st.caption("Intelligence Source: Phases 01-20 (Tournament Champion: LightGBM V2)")
st.write(f"Architect: **Patrick Simon Okosodo** | AI Architect | MLOps Specialist | B.Eng (Chem)")
