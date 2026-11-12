import streamlit as st
import numpy as np
import io
from scipy.io import wavfile

# App Title
st.title("🌌 NASA Space Apps: Multi-Tool Engineering Suite")

# Create Tabs for your projects
tab1, tab2, tab3 = st.tabs(["📡 Cosmic Static Messenger", "☄️ NEO Threat Matrix", "🔓 Signal Hacking Lab"])

# --- PROJECT 1: Cosmic Static Messenger ---
with tab1:
    st.header("Interplanetary Audio Messenger")
    st.write("Simulate sending text messages using FSK modulation through cosmic noise.")
    
    text_input = st.text_input("Enter message to transmit:", "Hello NASA Space Apps!")
    noise_level = st.slider("Cosmic Noise Intensity:", 0.0, 1.0, 0.15)

    if st.button("Transmit Message"):
        binary_data = ''.join(format(ord(char), '08b') for char in text_input)
        sample_rate = 8000
        duration_per_bit = 0.08
        t = np.linspace(0, duration_per_bit, int(sample_rate * duration_per_bit), endpoint=False)
        
        freq_0, freq_1 = 1200, 2200
        audio_signal = []
        for bit in binary_data:
            tone = np.sin(2 * np.pi * freq_0 * t) if bit == '0' else np.sin(2 * np.pi * freq_1 * t)
            audio_signal.extend(tone)
            
        audio_signal = np.array(audio_signal, dtype=np.float32)
        np.random.seed(42)
        noise = np.random.normal(0, noise_level, len(audio_signal))
        noisy_signal = audio_signal + noise
        audio_normalized = np.int16(noisy_signal / np.max(np.abs(noisy_signal)) * 32767)
        
        st.success("Transmitted successfully!")
        
        virtual_file = io.BytesIO()
        wavfile.write(virtual_file, sample_rate, audio_normalized)
        st.audio(virtual_file, format='audio/wav')
        
        # Receiver Decoding
        decoded_binary = ""
        chunk_size = int(sample_rate * duration_per_bit)
        for i in range(0, len(noisy_signal) - chunk_size + 1, chunk_size):
            chunk = noisy_signal[i:i + chunk_size]
            fft_vals = np.fft.rfft(chunk)
            fft_freqs = np.fft.rfftfreq(len(chunk), 1/sample_rate)
            peak_freq = fft_freqs[np.argmax(np.abs(fft_vals))]
            decoded_binary += '1' if peak_freq > 1700 else '0'
            
        decoded_text = ""
        for i in range(0, len(decoded_binary), 8):
            byte = decoded_binary[i:i+8]
            if len(byte) == 8:
                try: decoded_text += chr(int(byte, 2))
                except: decoded_text += '?'
                
        st.info(f"**Recovered Message:** `{decoded_text}`")

# --- PROJECT 2: NEO Threat Matrix (Dynamic Data) ---
with tab2:
    st.header("Near-Earth Object (NEO) Threat Matrix")
    st.write("Simulate asteroid trajectory risks and tracking metrics using real orbital profiles.")
    
    asteroid_name = st.selectbox("Select Asteroid Target:", ["Apophis (99942)", "Bennu (101955)", "Halley's Comet"])
    
    # Unique data dictionaries for each asteroid
    asteroid_data = {
        "Apophis (99942)": {
            "diameter": "340 meters", 
            "velocity": "30.7 km/s", 
            "threat": "MODERATE MONITORING", 
            "note": "⚠️ Close approach trajectory mapped for Earth orbit intersection monitoring."
        },
        "Bennu (101955)": {
            "diameter": "492 meters", 
            "velocity": "27.8 km/s", 
            "threat": "LOW / OSIRIS-REx Sampled", 
            "note": "✅ Orbital path verified by NASA OSIRIS-REx mission data."
        },
        "Halley's Comet": {
            "diameter": "11,000 meters", 
            "velocity": "54.6 km/s", 
            "threat": "DEEP SPACE / SECURE", 
            "note": "🌌 Periodic comet currently in outer solar system return trajectory."
        }
    }
    
    selected_info = asteroid_data[asteroid_name]
    
    st.write(f"**Analyzing telemetry data for {asteroid_name}...**")
    col1, col2, col3 = st.columns(3)
    col1.metric("Estimated Diameter", selected_info["diameter"])
    col2.metric("Relative Velocity", selected_info["velocity"])
    col3.metric("Threat Level", selected_info["threat"])
    
    st.warning(selected_info["note"])

# --- PROJECT 3: Signal Hacking & Decoding Lab ---
with tab3:
    st.header("🔓 Signal Hacking & External Decryption Lab")
    st.write("Decrypt external binary streams or intercepted audio files sent by other systems.")
    
    hack_mode = st.radio("Choose Hacking Method:", ["Decrypt Binary Stream Text", "Upload & Demodulate Audio File"])
    
    if hack_mode == "Decrypt Binary Stream Text":
        external_binary = st.text_area("Paste external 8-bit binary code here:", "01001000 01100101 01101100 01101100 01101110")
        if st.button("Crack Binary Code"):
            clean_bin = external_binary.replace(" ", "")
            cracked_text = ""
            for i in range(0, len(clean_bin), 8):
                byte = clean_bin[i:i+8]
                if len(byte) == 8:
                    try: cracked_text += chr(int(byte, 2))
                    except: cracked_text += '?'
            st.success(f"🔓 Successfully Cracked Text: `{cracked_text}`")
            
    else:
        uploaded_file = st.file_uploader("Upload external `.wav` transmission file:", type=["wav"])
        if uploaded_file is not None:
            sample_rate, data = wavfile.read(uploaded_file)
            st.audio(uploaded_file)
            
            if st.button("Run FFT Demodulator on Uploaded File"):
                if len(data.shape) > 1:
                    data = data[:, 0]
                    
                duration_per_bit = 0.08
                chunk_size = int(sample_rate * duration_per_bit)
                extracted_binary = ""
                
                for i in range(0, len(data) - chunk_size + 1, chunk_size):
                    chunk = data[i:i + chunk_size]
                    fft_vals = np.fft.rfft(chunk)
                    fft_freqs = np.fft.rfftfreq(len(chunk), 1/sample_rate)
                    peak_freq = fft_freqs[np.argmax(np.abs(fft_vals))]
                    extracted_binary += '1' if peak_freq > 1700 else '0'
                    
                final_cracked = ""
                for i in range(0, len(extracted_binary), 8):
                    byte = extracted_binary[i:i+8]
                    if len(byte) == 8:
                        try: final_cracked += chr(int(byte, 2))
                        except: final_cracked += '?'
                            
                st.success(f"🛰️ Intercepted Secret Message from File: `{final_cracked}`")