# Environmental Risk Prediction & Mapping

A Python project for predicting:
- Air pollution risk
- Water pollution risk
- Flood risk
- Geographic place-based risk mapping

This project uses machine learning and geospatial visualization to estimate risk levels for a selected location using environmental factors such as air quality, rainfall, proximity to water bodies, topography, and water quality indicators.

## Features
- Place-based prediction using latitude and longitude
- Prediction models for air pollution, water pollution, and flood risk
- Interactive map visualization
- Dashboard interface for environmental monitoring
- Synthetic sample data for quick prototype and testing

## Tech Stack
- Python
- Streamlit
- scikit-learn
- Pandas
- NumPy
- Plotly

## Project Structure

```bash
.
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
└── src
    ├── __init__.py
    ├── data_generator.py
    ├── modeling.py
    └── visualization.py
```

## Quick Start

1. Clone the repository
2. Create a virtual environment
3. Install dependencies
4. Run the app

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## How It Works

The project generates realistic synthetic environmental data for multiple places, trains one model per risk type, and predicts risk for a user-selected location.

Risk categories include:
- Air pollution risk based on AQI, PM2.5, NO2, SO2, and population density
- Water pollution risk based on pH, turbidity, nitrate, dissolved oxygen, and contamination indicators
- Flood risk based on rainfall, elevation, humidity, river proximity, and drainage conditions

## Example Inputs
- Latitude: 13.0674
- Longitude: 80.2376
- Air quality metrics
- Water quality metrics
- Rainfall and elevation

## Future Enhancements
- Connect with real government/environmental APIs
- Integrate satellite imagery or remote sensing data
- Add historical time-series forecasting
- Deploy as a web dashboard on cloud hosting
- Save predictions in a database

## License
This project is licensed under the MIT License.

## Suggested Use
This project is ideal for learning, portfolio building, and prototypes for environmental monitoring systems.

## Note
The default dataset is synthetic and designed to demonstrate the full workflow. To use real data, replace the generated dataset with actual field observations or public environmental datasets.
