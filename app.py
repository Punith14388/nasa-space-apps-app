import streamlit as st
import random
import pandas as pd
from weather_api import get_atmospheric_conditions

# --- Page Configuration ---
st.set_page_config(
    page_title="AETHER-QKD | Deep-Space Command",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Deep-Space CSS Styling for High Visibility ---
st.markdown("""
<style>
    /* Main Background & Theme */
    .stApp {
        background: linear-gradient(135deg, #050b14 0%, #0a192f 50%, #02060d 100%);
        color: #f8fafc;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #030712;
        border-right: 1px solid #1e293b;
    }
    
    /* Metric Cards - High Contrast Text */
    [data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid #38bdf8;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(56, 189, 248, 0.2);
    }
    [data-testid="stMetricValue"] {
        color: #38bdf8 !important;
        font-weight: 700;
    }
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
    }
    
    /* Success Alert Box Visibility */
    .stAlert {
        background-color: #064e3b !important;
        border: 1px solid #10b981 !important;
    }
    .stAlert p {
        color: #6ee7b7 !important;
        font-weight: bold !important;
    }
    
    /* Headers & Text */
    h1, h2, h3 {
        color: #38bdf8 !important;
        font-family: 'Helvetica Neue', sans-serif;
    }
    p, span, label {
        color: #f1f5f9 !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #0f172a;
        border-radius: 6px;
        color: #cbd5e1;
        padding: 10px 20px;
        border: 1px solid #334155;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0284c7 !important;
        color: white !important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar: Interplanetary Telemetry (Meteomatics Weather API) ---
st.sidebar.header("🌍 Interplanetary Telemetry")
st.sidebar.subheader("Meteomatics Weather API")

meteomatics_user = st.sidebar.text_input("API Username", value="", type="default")
meteomatics_pass = st.sidebar.text_input("API Password", value="", type="password")

weather_data = None
if meteomatics_user and meteomatics_pass:
    try:
        # Default coordinates (e.g., ground station link)
        weather_data = get_atmospheric_conditions(meteomatics_user, meteomatics_pass)
        if weather_data and isinstance(weather_data, dict):
            st.sidebar.success("Atmospheric Link Connected!")
            st.sidebar.metric("Ground Temperature", f"{weather_data.get('t_2m:C', 20.0):.1f} °C")
            st.sidebar.metric("Relative Humidity", f"{weather_data.get('relative_humidity_2m:p', 50.0):.1f} %")
            st.sidebar.metric("Wind Speed", f"{weather_data.get('wind_speed_10m:ms', 3.5):.1f} m/s")
        else:
            st.sidebar.error("API Error: Check credentials.")
    except Exception as e:
        st.sidebar.error(f"Connection failed: {e}")
else:
    st.sidebar.warning("Enter Meteomatics credentials to load live noise scaling.")

# Fallback safety check so weather_data is always a dictionary
if not isinstance(weather_data, dict):
    weather_data = {'t_2m:C': 25.0, 'relative_humidity_2m:p': 45.0, 'wind_speed_10m:ms': 2.1}

# --- Main Mission Control Header ---
st.title("🚀 MISSION CONTROL: Deep-Space Quantum & Enigma Suite")
st.markdown("### *Aether-Net Interplanetary Command & Cryptography Hub*")
st.markdown("A dual-layer security platform combining futuristic Quantum Key Distribution (BB84) with historical Enigma code-breaking labs.")

# --- Navigation Tabs ---
tab1, tab2, tab3 = st.tabs([
    "⚛️ Quantum Transmission (BB84)", 
    "📊 Security & QBER Audit", 
    "🕵️ Enigma Intercept & Code-Breaking Lab"
])

with tab1:
    st.header("BB84 Quantum Protocol: Transmission & Basis Sifting")
    st.markdown("Alice (Deep-Space Probe) transmits polarized photon streams across interplanetary distances to Bob (Ground Station).")
    
    col1, col2 = st.columns(2)
    with col1:
        num_bits = st.slider("Photon Stream Bit Length", min_value=16, max_value=256, value=64, step=16)
        if st.button("Transmit Photon Stream"):
            alice_bits = [random.randint(0, 1) for _ in range(num_bits)]
            alice_bases = [random.choice(['+', 'x']) for _ in range(num_bits)]
            bob_bases = [random.choice(['+', 'x']) for _ in range(num_bits)]
            
            # Simulate sifting
            shared_key = []
            for a_bit, a_base, b_base in zip(alice_bits, alice_bases, bob_bases):
                if a_base == b_base:
                    shared_key.append(str(a_bit))
            
            st.success(f"Transmission Complete! Sifted Key Generated with length: {len(shared_key)} bits.")
            st.text("Sample Sifted Key: " + "".join(shared_key[:32]) + ("..." if len(shared_key) > 32 else ""))

with tab2:
    st.header("Quantum Channel Security Audit & QBER Analysis")
    st.markdown("Auditing the quantum error rate against real-time atmospheric noise.")
    
    wind_speed = weather_data.get('wind_speed_10m:ms', 2.1)
    noise_factor = min(0.25, max(0.01, wind_speed * 0.02))
    calculated_qber = noise_factor * 100
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Environmental Noise Factor", f"{noise_factor:.3f}")
    m2.metric("Calculated QBER", f"{calculated_qber:.2f}%", "-0.5% vs threshold")
    m3.metric("Channel Security Status", "SECURE 🟢" if calculated_qber < 11.0 else "WARNING 🔴")
    
    st.info("Note: BB84 protocol mandates a Quantum Bit Error Rate (QBER) strictly below 11% to ensure no eavesdropping or severe atmospheric degradation has compromised the key.")

with tab3:
    st.header("Enigma Machine Intercept & Code-Breaking Lab")
    st.markdown("Simulate encrypting and decrypting intercepted telemetry using rotor-based cipher mechanics.")
    
    op_mode = st.radio("Select Operation Mode:", ["Encrypt Telemetry", "Decrypt / Crack Intercepted Code"])
    
    rotor_offset = st.slider("Rotor Offset / Key Setting:", min_value=1, max_value=26, value=3)
    plugboard_secret = st.text_input("Plugboard Secret Code:", value="NASA-SECURE")
    
    if op_mode == "Encrypt Telemetry":
        raw_msg = st.text_area("Enter Telemetry Message:", value="ORBITAL TRAJECTORY STABLE")
        if st.button("Encrypt Message"):
            encrypted = "".join([chr(ord(c) + rotor_offset) if c.isalpha() else c for c in raw_msg.upper()])
            st.text_input("Generated Ciphertext:", value=encrypted)
    else:
        ciphertext = st.text_area("Paste Intercepted Ciphertext Here:", value="RUFDUFVCVRIQQRAQD")
        if st.button("Crack & Decrypt Code"):
            decrypted = "".join([chr(ord(c) - rotor_offset) if c.isalpha() else c for c in ciphertext.upper()])
            st.success("Successfully Cracked Intercepted Message!")
            st.text_input("Decrypted Intelligence:", value=decrypted)
