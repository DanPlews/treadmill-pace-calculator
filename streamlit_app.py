import streamlit as st

# Load ENDÜROX logo
st.image("logo.png", width=250)

st.markdown("### Built for real-world athletes. Backed by science.")
st.title("🏃‍♂️ Treadmill Pace Equivalence Calculator")

st.markdown("""
This calculator helps you determine what pace and speed you should run on a treadmill at different inclines, 
matching the same physiological effort. Toggle between metric and imperial units.
""")

# --- Helper Functions ---
def min_per_unit_to_speed(min_per_unit):
    return 60 / min_per_unit  # speed in units/hour

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

# --- Unit Toggle ---
unit = st.radio("Choose units", ["Metric (km)", "Imperial (mi)"], horizontal=True)

is_metric = unit == "Metric (km)"
unit_label = "min/km" if is_metric else "min/mi"
speed_unit = "km/h" if is_metric else "mph"

# --- Input ---
st.markdown("#### Reference Inputs")
pace_min = st.number_input(f"Pace ({unit_label})", min_value=2.0, max_value=15.0, value=5.0, step=0.1)
incline_ref = st.number_input("Incline (%)", min_value=0.0, max_value=15.0, value=1.5, step=0.1)

# --- Convert to metric for calculation ---
# If imperial, convert miles to km (1 mile = 1.60934 km)
pace_metric = pace_min * 1.60934 if not is_metric else pace_min
speed_kmh = min_per_unit_to_speed(pace_metric)

# --- VO2 reference ---
speed_m_per_min = (speed_kmh * 1000) / 60
vo2_ref = calculate_vo2(speed_m_per_min, incline_ref)

# --- Output Speed & Pace Format ---
speed_display = speed_kmh if is_metric else speed_kmh / 1.60934
pace_str = speed_to_min_per_unit(speed_display)

col1, col2 = st.columns(2)
col1.metric(label=f"Treadmill Speed ({speed_unit})", value=f"{speed_display:.2f}")
col2.metric(label=f"Pace Format ({unit_label})", value=pace_str)

# --- Equivalent Table ---
st.markdown("---")
st.subheader(f"Equivalent Speeds at Other Inclines ({speed_unit})")

for i in range(1, 11):
    eq_speed_kmh = calculate_equivalent_speed(vo2_ref, i)
    eq_speed = eq_speed_kmh if is_metric else eq_speed_kmh / 1.60934
    eq_pace = speed_to_min_per_unit(eq_speed)
    st.write(f"**{i}% incline** → {eq_speed:.2f} {speed_unit} ({eq_pace} per { 'km' if is_metric else 'mi'})")

# --- Hide Streamlit UI ---
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)
