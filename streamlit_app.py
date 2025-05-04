import streamlit as st

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

st.title("🏃‍♂️ Treadmill Pace Equivalence Calculator")

st.markdown("""
Select a reference pace and incline, and we'll show you the treadmill speed and equivalent paces at other inclines to match the same VO₂ cost.
""")

# Inputs
pace_min = st.number_input("Reference Pace (min/km)", min_value=2.0, max_value=10.0, value=3.5, step=0.1)
incline_ref = st.number_input("Reference Incline (%)", min_value=0.0, max_value=15.0, value=1.5, step=0.1)

# Convert to speed and formatted pace
speed_kmh = min_per_km_to_speed(pace_min)
formatted_pace = min_per_km_to_str(pace_min)

st.metric(label="🛞 Treadmill Speed", value=f"{speed_kmh} km/h")
st.metric(label="🕒 Pace Format", value=formatted_pace)

# Calculate reference VO₂
speed_m_per_min = 1000 / pace_min
vo2_ref = 3.5 + 0.2 * speed_m_per_min + 0.9 * speed_m_per_min * (incline_ref / 100)

# Output table
st.subheader("Equivalent Speeds at Other Inclines")
for i in range(1, 11):
    speed, pace = calculate_equivalent_speed(vo2_ref, i)
    st.write(f"**{i}% incline** → {speed} km/h ({pace})")
