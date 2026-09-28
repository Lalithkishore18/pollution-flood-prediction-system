import numpy as np
import pandas as pd


def generate_environmental_data(n_samples=1500, seed=42):
    rng = np.random.default_rng(seed)

    df = pd.DataFrame({
        "latitude": rng.uniform(8.0, 30.0, n_samples),
        "longitude": rng.uniform(68.0, 95.0, n_samples),
        "population_density": rng.uniform(200, 18000, n_samples),
        "industry_distance_km": rng.uniform(0.5, 40.0, n_samples),
        "elevation_m": rng.uniform(0, 500, n_samples),
        "rainfall_mm": rng.uniform(400, 2600, n_samples),
        "temperature_c": rng.uniform(18, 38, n_samples),
        "humidity_pct": rng.uniform(35, 95, n_samples),
        "pm25": rng.uniform(5, 220, n_samples),
        "no2": rng.uniform(3, 180, n_samples),
        "so2": rng.uniform(2, 140, n_samples),
        "air_quality_index": rng.uniform(20, 260, n_samples),
        "water_ph": rng.normal(7.2, 1.1, n_samples),
        "turbidity_ntu": rng.uniform(2, 120, n_samples),
        "dissolved_oxygen_mg_l": rng.uniform(1.5, 12.0, n_samples),
        "nitrate_mg_l": rng.uniform(1.0, 30.0, n_samples),
        "distance_to_river_km": rng.uniform(0.1, 30.0, n_samples),
    })

    df["air_quality_index"] = (
        25
        + 0.55 * df["pm25"]
        + 0.52 * df["no2"]
        + 0.45 * df["so2"]
        + (12000 / (df["industry_distance_km"] + 1)) * 0.08
        + (df["population_density"] / 100) * 0.15
        + rng.normal(0, 15, n_samples)
    )

    df["water_ph"] = np.clip(df["water_ph"], 3.0, 10.0)
    df["turbidity_ntu"] = np.clip(df["turbidity_ntu"], 1.0, 150.0)
    df["dissolved_oxygen_mg_l"] = np.clip(df["dissolved_oxygen_mg_l"], 0.5, 15.0)
    df["nitrate_mg_l"] = np.clip(df["nitrate_mg_l"], 0.1, 40.0)

    df["air_pollution_risk"] = (
        (df["air_quality_index"] > 90)
        | (df["pm25"] > 65)
        | (df["no2"] > 45)
        | (df["so2"] > 30)
    ).astype(int)

    df["water_pollution_risk"] = (
        (df["water_ph"] < 6.5)
        | (df["water_ph"] > 8.5)
        | (df["turbidity_ntu"] > 35)
        | (df["dissolved_oxygen_mg_l"] < 4)
        | (df["nitrate_mg_l"] > 15)
    ).astype(int)

    df["flood_risk"] = (
        (df["rainfall_mm"] > 1500)
        | (df["humidity_pct"] > 80)
        | (df["distance_to_river_km"] < 2)
        | (df["elevation_m"] < 30)
    ).astype(int)

    return df


if __name__ == "__main__":
    frame = generate_environmental_data()
    print(frame.head())
