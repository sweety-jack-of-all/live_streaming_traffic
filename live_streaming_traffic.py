import streamlit as st
import requests
import pandas as pd
import numpy as np
import time
from datetime import datetime
import plotly.express as px

# Set Streamlit page config
st.set_page_config(page_title="Live Traffic Data", layout="wide")
st.title("🚦 Live Traffic Stream")

# TomTom API credentials
API_KEY = "Tc0H8xHKFvJz77pQaWrcXLUhfMLGqt26"  # Replace with your TomTom API key
LATITUDE = 51.5074  # Example latitude (London)
LONGITUDE = -0.1278  # Example longitude (London)
RADIUS = 1000  # Radius in meters for traffic data

# Function to fetch traffic data from TomTom API
def fetch_traffic_data():
    url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?point={LATITUDE},{LONGITUDE}&radius={RADIUS}&key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    # Parse the necessary data
    if response.status_code == 200 and data.get('flowSegmentData'):
        flow_data = data['flowSegmentData']
        return {
            'time': datetime.now(),
            'traffic_density': flow_data.get('currentSpeed'),
            'avg_speed': flow_data.get('freeFlowSpeed')
        }
    else:
        st.warning("Failed to fetch traffic data.")
        return None

# Initialize session state for holding live data
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["time", "traffic_density", "avg_speed"])

# Placeholder for chart
chart_placeholder = st.empty()

# Stream for live traffic data updates
for _ in range(100):  # You can adjust the range for how long you want to stream
    new_data = fetch_traffic_data()
    
    if new_data:
        # Append new data to session state
        st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_data])]).tail(50)

        # Plot live traffic data
        chart_placeholder.line_chart(
            st.session_state.data.set_index("time")[["traffic_density", "avg_speed"]]
        )

    # Wait for 1 second before fetching new data
    time.sleep(1)
