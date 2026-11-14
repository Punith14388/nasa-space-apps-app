import streamlit as st
from weather_api import get_atmospheric_conditions

# --- Sidebar Configuration for Meteomatics Weather API ---
st.sidebar.header("🌍 Interplanetary Telemetry")
st.sidebar.subheader("Meteomatics Weather API")

# Input fields for API credentials
meteomatics_user = st.sidebar.text_input("API Username", value="", type="default")
meteomatics_pass = st.sidebar.text_input("API Password", value="", type="password")

# Fetch and validate connection
weather_data = None
if meteomatics_user and meteomatics_pass:
    try:
        # Fetch live data using default coordinates (e.g., ground station / target location)
        weather_data = get_atmospheric_conditions(meteomatics_user, meteomatics_pass)
        if weather_data:
            st.sidebar.success("Atmospheric Link Connected!")
            st.sidebar.metric("Ground Temperature", f"{weather_data.get('t_2m:C', 0):.1f} °C")
            st.sidebar.metric("Relative Humidity", f"{weather_data.get('relative_humidity_2m:p', 0):.1f} %")
            st.sidebar.metric("Wind Speed", f"{weather_data.get('wind_speed_10m:ms', 0):.1f} m/s")
        else:
            st.sidebar.error("API Error: Check credentials or endpoint.")
    except Exception as e:
        st.sidebar.error(f"Connection failed: {e}")
else:
    st.sidebar.warning("Please enter your Meteomatics API credentials to enable live noise scaling.")
