# treadmill-pace-calculator
import streamlit as st

def calculate_equivalent_speed(vo2_ref, incline_percent):
    incline_decimal = incline_percent / 100
    x = (vo2_ref - 3.5) / (0.2 + 0.9 * incline_decimal)
    m_per_min = x
    km_per_h = (m_per_min * 60) / 1000
    min_per_km = 60 / km_per_h
    return round(km_per_h, 2), f"{int(min_per_km)}:{int((min_per_km % 1) * 60):02d}/km"

st.title("🏃‍♂️ Treadmill Pace Equivalence Calculator")

st.markdown("""
This calculator helps you determine what pace you should run on the treadmill at different inclines
to match the same physiological intensity (VO₂ demand) as your target reference pace and incline.
""")

# Input: reference pace and incline
pace_min = st.number_input("Reference Pace (min/km)", min_value=2.0, max_value=10.0, value=3.5, step=0.1)
incline_ref = st.number_input("Reference Incline (%)", min_value=0.0, max_value=15.0, value=1.5, step=0.1)

# Calculate VO2 from reference
speed_m_per_min = 1000 / pace_min
vo2_ref = 3.5 + 0.2 * speed_m_per_min + 0.9 * speed_m_per_min * (incline_ref / 100)

st.subheader("Equivalent Speeds at Other Inclines")

# Table output
st.write("For the same VO₂, here's the equivalent speed at each incline:")

for i in range(1, 11):
    speed, pace = calculate_equivalent_speed(vo2_ref, i)
    st.write(f"**{i}% incline** → {speed} km/h ({pace})")

