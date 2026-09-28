import streamlit as st
import pandas as pd

from src.data_generator import generate_environmental_data
from src.modeling import train_models, predict_environmental_risk
from src.visualization import build_map_figure, build_risk_bar_chart


st.set_page_config(
    page_title="Environmental Risk Predictor",
    page_icon="🌍",
    layout="wide",
)

st.title("🌍 Environmental Risk Prediction & Mapping")
st.caption("Predict air pollution, water pollution, and flood risk for a specific place.")

@st.cache_data
def load_data():
    return generate_environmental_data(n_samples=1500, seed=42)

@st.cache_resource
def load_models():
    df = load_data()
    return train_models(df)


df = load_data()
models = load_models()

with st.sidebar:
    st.header("Location Details")
    latitude = st.number_input("Latitude", min_value=-90.0, max_value=90.0, value=13.0674, step=0.0001)
    longitude = st.number_input("Longitude", min_value=-180.0, max_value=180.0, value=80.2376, step=0.0001)
    population_density = st.number_input("Population Density", min_value=0, max_value=50000, value=4200, step=10)
    rainfall_mm = st.number_input("Rainfall (mm)", min_value=0.0, max_value=5000.0, value=1350.0, step=10.0)
    temperature_c = st.number_input("Temperature (°C)", min_value=-20.0, max_value=60.0, value=31.2, step=0.1)
    humidity_pct = st.number_input("Humidity (%)", min_value=0, max_value=100, value=78, step=1)
    elevation_m = st.number_input("Elevation (m)", min_value=-50.0, max_value=5000.0, value=55.0, step=1.0)
    distance_to_river_km = st.number_input("Distance to River (km)", min_value=0.0, max_value=100.0, value=4.5, step=0.1)

    st.header("Air Quality")
    pm25 = st.number_input("PM2.5 (μg/m³)", min_value=0.0, max_value=300.0, value=72.0, step=1.0)
    no2 = st.number_input("NO₂ (μg/m³)", min_value=0.0, max_value=300.0, value=58.0, step=1.0)
    so2 = st.number_input("SO₂ (μg/m³)", min_value=0.0, max_value=250.0, value=39.0, step=1.0)
    aqi = st.number_input("AQI", min_value=0, max_value=500, value=110, step=1)

    st.header("Water Quality")
    water_ph = st.number_input("Water pH", min_value=0.0, max_value=14.0, value=7.5, step=0.1)
    turbidity_ntu = st.number_input("Turbidity (NTU)", min_value=0.0, max_value=200.0, value=32.0, step=1.0)
    dissolved_oxygen = st.number_input("Dissolved Oxygen (mg/L)", min_value=0.0, max_value=20.0, value=5.6, step=0.1)
    nitrate = st.number_input("Nitrate (mg/L)", min_value=0.0, max_value=50.0, value=11.5, step=0.1)

    st.header("Site Characteristics")
    industry_distance_km = st.number_input("Distance to Industry (km)", min_value=0.0, max_value=100.0, value=12.0, step=0.1)

    predict_button = st.button("Predict Risks", use_container_width=True)

col1, col2, col3 = st.columns(3)

if predict_button:
    sample = {
        "latitude": latitude,
        "longitude": longitude,
        "population_density": population_density,
        "industry_distance_km": industry_distance_km,
        "elevation_m": elevation_m,
        "rainfall_mm": rainfall_mm,
        "temperature_c": temperature_c,
        "humidity_pct": humidity_pct,
        "pm25": pm25,
        "no2": no2,
        "so2": so2,
        "air_quality_index": aqi,
        "water_ph": water_ph,
        "turbidity_ntu": turbidity_ntu,
        "dissolved_oxygen_mg_l": dissolved_oxygen,
        "nitrate_mg_l": nitrate,
        "distance_to_river_km": distance_to_river_km,
    }

    predictions = predict_environmental_risk(models, sample)

    for idx, risk_name in enumerate(["air_pollution_risk", "water_pollution_risk", "flood_risk"]):
        label = predictions[risk_name]["label"]
        prob = predictions[risk_name]["probability"]
        color = {
            "Low": "green",
            "Moderate": "orange",
            "High": "red",
        }.get(label, "gray")

        with [col1, col2, col3][idx]:
            st.markdown(
                f"<div style='padding: 1rem; border-radius: 12px; background-color: #{'f5f5f5' if color == 'green' else 'fff3e0' if color == 'orange' else 'fdecea'}; border: 1px solid {color};'>"
                f"<h4>{risk_name.replace('_', ' ').title()}</h4>"
                f"<h3 style='color: {color};'>{label}</h3>"
                f"<p>Probability: {prob:.2%}</p>"
                f"</div>",
                unsafe_allow_html=True,
            )

    risk_bar_chart = build_risk_bar_chart(predictions)
    st.plotly_chart(risk_bar_chart, use_container_width=True)

    map_figure = build_map_figure(df, prediction_point=(latitude, longitude))
    st.plotly_chart(map_figure, use_container_width=True)

else:
    st.info("Choose the location details and click 'Predict Risks' to view the output.")

    st.write("### Sample Data Overview")
    st.dataframe(df.head(10), use_container_width=True)

    st.write("### Map Overview")
    map_figure = build_map_figure(df, prediction_point=(13.0674, 80.2376))
    st.plotly_chart(map_figure, use_container_width=True)
