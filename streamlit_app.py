import streamlit as st

# --- Branding ---
st.image("logo.png", width=250)
st.markdown("### Science in Strength. Experts in Endurance.")
st.title("Treadmill Pace Equivalence Calculator for Inclines")

st.markdown("""
This calculator helps you determine what pace and speed you should run on a treadmill at different inclines, 
matching the same physiological effort. The reference inputs set refers to the intensity you are trying to replicate. Toggle between metric and imperial units.
""")

# --- Helper Functions ---
def min_per_unit_to_speed(min_per_unit):
    return 60 / min_per_unit

def speed_to_min_per_unit(speed):
    min_per_unit = 60 / speed
    minutes = int(min_per_unit)
    seconds = int(round((min_per_unit - minutes) * 60))
    return f"{minutes}:{seconds:02d}"

def calculate_vo2(speed_m_per_min, incline_percent):
    return 3.5 + 0.2 * speed_m_per_min + 0.9 * speed_m_per_min * (incline_percent / 100)

def calculate_equivalent_speed(vo2_ref, incline_percent):
    incline_decimal = incline_percent / 100
    x = (vo2_ref - 3.5) / (0.2 + 0.9 * incline_decimal)
    m_per_min = x
    km_per_h = (m_per_min * 60) / 1000
    return km_per_h

# --- Unit Selection ---
unit = st.radio("Choose units", ["Metric (km)", "Imperial (mi)"], horizontal=True)
is_metric = unit == "Metric (km)"
unit_label = "min/km" if is_metric else "min/mi"
speed_unit = "km/h" if is_metric else "mph"

# --- Inputs ---
st.markdown("#### Reference Inputs")
pace_min = st.number_input(f"Pace ({unit_label})", min_value=2.0, max_value=15.0, value=5.0, step=0.1)
incline_ref = st.number_input("Incline (%)", min_value=0.0, max_value=15.0, value=1.5, step=0.1)

# --- Correct Speed Conversion ---
if is_metric:
    speed = min_per_unit_to_speed(pace_min)  # km/h
    speed_kmh = speed
else:
    speed = min_per_unit_to_speed(pace_min)  # mph
    speed_kmh = speed * 1.60934  # convert to km/h for VO2

# --- VO2 Reference ---
speed_m_per_min = (speed_kmh * 1000) / 60
vo2_ref = calculate_vo2(speed_m_per_min, incline_ref)

# --- Display Speed & Pace Format ---
pace_str = speed_to_min_per_unit(speed)
col1, col2 = st.columns(2)
col1.metric(label=f"Treadmill Speed ({speed_unit})", value=f"{speed:.2f}")
col2.metric(label=f"Pace Format ({unit_label})", value=pace_str)

# --- Table of Equivalent Speeds ---
st.markdown("---")
st.subheader(f"Equivalent Speeds at Other Inclines ({speed_unit})")

for i in range(1, 11):
    eq_speed_kmh = calculate_equivalent_speed(vo2_ref, i)
    eq_speed = eq_speed_kmh if is_metric else eq_speed_kmh / 1.60934
    eq_pace = speed_to_min_per_unit(eq_speed)
    st.write(f"**{i}% incline** → {eq_speed:.2f} {speed_unit} ({eq_pace} per {'km' if is_metric else 'mi'})")

# --- Hide Streamlit UI ---
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)
