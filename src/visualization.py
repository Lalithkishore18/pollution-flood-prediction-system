from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def prepare_features(df):
    feature_columns = [
        "latitude",
        "longitude",
        "population_density",
        "industry_distance_km",
        "elevation_m",
        "rainfall_mm",
        "temperature_c",
        "humidity_pct",
        "pm25",
        "no2",
        "so2",
        "air_quality_index",
        "water_ph",
        "turbidity_ntu",
        "dissolved_oxygen_mg_l",
        "nitrate_mg_l",
        "distance_to_river_km",
    ]
    return df[feature_columns]


def train_models(df):
    X = prepare_features(df)

    targets = {
        "air_pollution_risk": df["air_pollution_risk"],
        "water_pollution_risk": df["water_pollution_risk"],
        "flood_risk": df["flood_risk"],
    }

    models = {}
    scores = {}

    for target_name, y in targets.items():
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        model = RandomForestClassifier(
            n_estimators=250,
            random_state=42,
            max_depth=10,
            min_samples_leaf=2,
        )
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        models[target_name] = model
        scores[target_name] = acc

    return {"models": models, "scores": scores}


def predict_environmental_risk(model_bundle, sample_data):
    X = {
        "latitude": sample_data.get("latitude", 0.0),
        "longitude": sample_data.get("longitude", 0.0),
        "population_density": sample_data.get("population_density", 0.0),
        "industry_distance_km": sample_data.get("industry_distance_km", 0.0),
        "elevation_m": sample_data.get("elevation_m", 0.0),
        "rainfall_mm": sample_data.get("rainfall_mm", 0.0),
        "temperature_c": sample_data.get("temperature_c", 0.0),
        "humidity_pct": sample_data.get("humidity_pct", 0.0),
        "pm25": sample_data.get("pm25", 0.0),
        "no2": sample_data.get("no2", 0.0),
        "so2": sample_data.get("so2", 0.0),
        "air_quality_index": sample_data.get("air_quality_index", 0.0),
        "water_ph": sample_data.get("water_ph", 7.0),
        "turbidity_ntu": sample_data.get("turbidity_ntu", 0.0),
        "dissolved_oxygen_mg_l": sample_data.get("dissolved_oxygen_mg_l", 0.0),
        "nitrate_mg_l": sample_data.get("nitrate_mg_l", 0.0),
        "distance_to_river_km": sample_data.get("distance_to_river_km", 0.0),
    }

    feature_order = [
        "latitude",
        "longitude",
        "population_density",
        "industry_distance_km",
        "elevation_m",
        "rainfall_mm",
        "temperature_c",
        "humidity_pct",
        "pm25",
        "no2",
        "so2",
        "air_quality_index",
        "water_ph",
        "turbidity_ntu",
        "dissolved_oxygen_mg_l",
        "nitrate_mg_l",
        "distance_to_river_km",
    ]

    row = [X[col] for col in feature_order]

    results = {}
    for risk_name, model in model_bundle["models"].items():
        probability = model.predict_proba([row])[0]
        cls = model.classes_
        risk_score = probability[1] if len(cls) > 1 and 1 in cls else probability.max()
        pred = int(model.predict([row])[0])
        if pred == 0:
            label = "Low"
        elif pred == 1:
            label = "High"
        else:
            label = "Moderate"
        results[risk_name] = {
            "label": label,
            "probability": float(risk_score),
        }

    return results
