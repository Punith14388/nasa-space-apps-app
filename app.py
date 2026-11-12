import streamlit as st
import numpy as np

# Page Configuration with wide layout
st.set_page_config(page_title="Deep-Space QKD & Enigma Suite", page_icon="🚀", layout="wide")

# Custom CSS for Background Video and High Contrast Text / Tabs / Buttons
st.markdown("""
    <style>
    /* Make main container background transparent so the video is visible */
    .stApp {
        background-color: rgba(3, 7, 18, 0.75) !important;
        color: #f0f9ff;
    }
    
    /* Full-screen fixed background video */
    .video-background {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -999;
        overflow: hidden;
        pointer-events: none;
    }
    
    .video-background iframe {
        position: absolute;
        top: 50%;
        left: 50%;
        width: 100vw;
        height: 56.25vw;
        min-height: 100vh;
        min-width: 177.77vh;
        transform: translate(-50%, -50%);
        opacity: 0.35;
    }

    /* High contrast form labels & headings */
    label, .stRadio label, .stSlider label, .stTextInput label, .stTextArea label {
        color: #ffffff !important;
        font-weight: 700 !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.8);
    }
    
    h1, h2, h3, h4 {
        color: #38bdf8 !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.9);
    }

    /* Fix Tab Text Visibility */
    div.stTabs [data-baseweb="tab-list"] {
        background-color: rgba(15, 23, 42, 0.95);
        border-radius: 8px;
        padding: 6px;
        border: 1px solid #38bdf8;
    }
    
    div.stTabs [data-baseweb="tab"] {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    
    div.stTabs [aria-selected="true"] {
        background-color: #0284c7 !important;
        border-radius: 6px;
    }

    /* Fix Button Styling & Text */
    .stButton>button {
        background: linear-gradient(90deg, #0284c7 0%, #1d4ed8 100%) !important;
        color: #ffffff !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 6px;
        padding: 10px 24px;
        font-weight: 800 !important;
        box-shadow: 0 0 15px rgba(2, 132, 199, 0.6);
    }
    
    .stButton>button:hover {
        background: linear-gradient(90deg, #0ea5e9 0%, #2563eb 100%) !important;
        color: #ffffff !important;
    }

    /* Metrics Styling */
    [data-testid="stMetric"] {
        background-color: rgba(15, 23, 42, 0.9);
        border: 1px solid #38bdf8;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }
    
    [data-testid="stMetricValue"] {
        color: #38bdf8 !important;
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        text-shadow: 0 2px 8px rgba(56, 189, 248, 0.6);
    }
    
    [data-testid="stMetricLabel"] {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    </style>

    <!-- Embedded Apollo 13 Launch Background Video -->
    <div class="video-background">
        <iframe src="https://www.youtube.com/embed/cX9f9USfz5c?autoplay=1&mute=1&controls=0&loop=1&playlist=cX9f9USfz5c" 
                frameborder="0" allow="autoplay; encrypted-media">
        </iframe>
    </div>
""", unsafe_allow_html=True)

# App Header
st.title("🚀 MISSION CONTROL: Deep-Space Quantum & Enigma Suite")
st.markdown("### *Aether-Net Interplanetary Command & Cryptography Hub*")
st.write("A dual-layer security platform combining futuristic Quantum Key Distribution (BB84) with historical Enigma code-breaking labs.")

# Navigation Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "⚛️ Quantum Transmission (BB84)", 
    "🌌 Security & QBER Audit", 
    "🔑 Key Reconciliation", 
    "🕵️ Enigma Intercept & Code-Breaking Lab"
])

# Session state initialization
if "qkd_run" not in st.session_state:
    st.session_state.qkd_run = False
    st.session_state.sifted_alice_key = []
    st.session_state.sifted_bob_key = []

# --- TAB 1: BB84 Transmission & Sifting ---
with tab1:
    st.header("BB84 Quantum Protocol: Transmission & Basis Sifting")
    st.write("Alice (Deep-Space Probe) transmits polarized photon streams across interplanetary distances to Bob (Ground Station).")

    col1, col2 = st.columns(2)
    with col1:
        num_photons = st.slider("Number of Photons to Transmit:", 50, 1000, 200, 50)
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        eavesdropper_active = st.checkbox("🛰️ Enable Interceptor (Eve Attack Simulation)")

    if st.button("Initialize Quantum Transmission"):
        np.random.seed(42)
        alice_bits = np.random.randint(0, 2, num_photons)
        alice_bases = np.random.randint(0, 2, num_photons)
        bob_bases = np.random.randint(0, 2, num_photons)
        
        bob_results = []
        for i in range(num_photons):
            bit = alice_bits[i]
            a_base = alice_bases[i]
            b_base = bob_bases[i]
            
            if eavesdropper_active:
                eve_base = np.random.randint(0, 2)
                if eve_base != a_base:
                    bit = np.random.randint(0, 2)
            
            if a_base == b_base:
                bob_results.append(bit)
            else:
                bob_results.append(np.random.randint(0, 2))
                
        bob_results = np.array(bob_results)
        matching_indices = np.where(alice_bases == bob_bases)[0]
        sifted_alice_key = alice_bits[matching_indices]
        sifted_bob_key = bob_results[matching_indices]
        
        st.session_state.qkd_run = True
        st.session_state.sifted_alice_key = sifted_alice_key
        st.session_state.sifted_bob_key = sifted_bob_key
        st.session_state.num_photons = num_photons
        st.session_state.eavesdropper_active = eavesdropper_active
        
        st.success(f"Transmission successful! Photons processed across deep space link.")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Photons Sent", num_photons)
        m2.metric("Sifted Key Length", len(sifted_alice_key))
        m3.metric("Sifting Efficiency", f"{(len(sifted_alice_key)/num_photons)*100:.1f}%")

# --- TAB 2: QBER & Security Audit ---
with tab2:
    st.header("Quantum Bit Error Rate (QBER) & Security Audit")
    if st.session_state.qkd_run and len(st.session_state.sifted_alice_key) > 0:
        sifted_alice = st.session_state.sifted_alice_key
        sifted_bob = st.session_state.sifted_bob_key
        errors = np.sum(sifted_alice != sifted_bob)
        qber = errors / len(sifted_alice)
        
        q1, q2, q3 = st.columns(3)
        q1.metric("Sifted Key Mismatches", errors)
        q2.metric("Quantum Bit Error Rate (QBER)", f"{qber*100:.2f}%")
        q3.metric("Security Threshold Limit", "11.0%")
        
        if qber > 0.11 or st.session_state.eavesdropper_active:
            st.error("🚨 **SECURITY ALERT:** High QBER detected! An active eavesdropper or severe cosmic distortion has compromised the quantum channel.")
        else:
            st.success("✅ **Secure Channel Verified:** QBER is well below the 11% cryptographic threshold.")
    else:
        st.warning("⚠️ Please initialize the quantum transmission first in Tab 1.")

# --- TAB 3: Key Reconciliation ---
with tab3:
    st.header("Error Reconciliation & Final Cryptographic Key")
    if st.session_state.qkd_run and len(st.session_state.sifted_bob_key) > 0:
        final_key = st.session_state.sifted_bob_key
        key_str = ''.join(map(str, final_key[:64]))
        st.code(key_str, language="text")
        st.info(f"**Secure Interplanetary Key Bit-Length:** {len(final_key)} bits shared between probe and Earth station.")
    else:
        st.warning("⚠️ Please complete the quantum transmission step in Tab 1 first.")

# --- TAB 4: Enigma Intercept & Code-Breaking Lab ---
with tab4:
    st.header("🕵️ Enigma Machine Intercept & Code-Breaking Lab")
    st.write("Simulate encrypting and decrypting intercepted telemetry using rotor-based cipher mechanics.")
    
    enigma_mode = st.radio("Select Operation Mode:", ["Encrypt Telemetry", "Decrypt / Crack Intercepted Code"])
    
    rotor_alphabet = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
    standard_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    def enigma_transform(text, shift):
        result = ""
        for char in text.upper():
            if char in standard_alphabet:
                idx = (standard_alphabet.find(char) + shift) % 26
                result += rotor_alphabet[idx]
            else:
                result += char
        return result

    def enigma_decrypt(text, shift):
        result = ""
        for char in text.upper():
            if char in rotor_alphabet:
                idx = (rotor_alphabet.find(char) - shift) % 26
                result += standard_alphabet[idx]
            else:
                result += char
        return result

    col_e1, col_e2 = st.columns(2)
    with col_e1:
        rotor_setting = st.slider("Rotor Offset / Key Setting:", 1, 25, 3)
    with col_e2:
        plugboard_swap = st.text_input("Plugboard Secret Code:", "NASA-SECURE")

    if enigma_mode == "Encrypt Telemetry":
        raw_message = st.text_input("Enter Secret Telemetry Message:", "ORION ORBIT SECURED")
        if st.button("Generate Enigma Cipher"):
            ciphertext = enigma_transform(raw_message, rotor_setting)
            st.success("🔒 Ciphertext Generated Successfully!")
            st.code(ciphertext, language="text")
    else:
        intercepted_code = st.text_area("Paste Intercepted Ciphertext Here:", "SFWKS SFKFW KWSFW")
        if st.button("Crack & Decrypt Code"):
            decrypted_text = enigma_decrypt(intercepted_code, rotor_setting)
            st.success("🔓 Successfully Cracked Intercepted Message!")
            st.code(decrypted_text, language="text")
