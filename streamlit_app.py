import streamlit as st
from PIL import Image

# Load and display logo
logo = Image.open("Logo Black.png")
st.image(logo, use_column_width=False, width=250)

st.markdown("### Built for real-world athletes. Backed by science.")
st.title("🏃‍♂️ Treadmill Pace Equivalence Calculator")

st.markdown("""
Use this calculator to find the treadmill speed or equivalent incline pace that matches your target training intensity.
""")

# Convert functions
def calculate_equivalent_speed(vo2_ref, incline_percent):
    incline_decimal = incline_percent / 100
    x = (vo2_ref - 3.5) / (0.2 + 0.9 * incline_decimal)
    m_per_min = x
    km_per_h = (m_per_min * 60) / 1000
    min_per_km = 60 / km_per_h
    return round(km_per_h, 2), f"{int(min_per_km)}:{int((min_per_km % 1) * 60):02d}/km"

def min_per_km_to_speed(min_per_km):
    speed = 60 / min_per_km
    return round(speed, 2)

def min_per_km_to_str(min_per_km):
    minutes = int(min_per_km)
    seconds = int(round((min_per_km - minutes) * 60))
    return f"{minutes}:{seconds:02d}/km"

# User input
st.markdown("#### Reference Inputs")
pace_min = st.number_input("Pace (min/km)", min_value=2.0, max_value=10.0, value=3.5, step=0.1)
incline_ref = st.number_input("Incline (%)", min_value=0.0, max_value=15.0, value=1.5, step=0.1)

# Calculate reference speed and pace
speed_kmh = min_per_km_to_speed(pace_min)
formatted_pace = min_per_km_to_str(pace_min)

# Show metrics
col1, col2 = st.columns(2)
col1.metric(label="Treadmill Speed", value=f"{speed_kmh} km/h")
col2.metric(label="Pace Format", value=formatted_pace)

# VO2 Calculation
speed_m_per_min = 1000 / pace_min
vo2_ref = 3.5 + 0.2 * speed_m_per_min + 0.9 * speed_m_per_min * (incline_ref / 100)

st.markdown("---")
st.subheader("Equivalent Speeds at Other Inclines")

for i in range(1, 11):
    speed, pace = calculate_equivalent_speed(vo2_ref, i)
    st.write(f"**{i}% incline** → {speed} km/h ({pace})")

# Hide Streamlit footer and menu
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)
