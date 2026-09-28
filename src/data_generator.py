import plotly.express as px
import plotly.graph_objects as go


def build_map_figure(df, prediction_point=None):
    df_for_map = df.copy()
    df_for_map["overall_risk"] = (
        0.4 * df_for_map["air_pollution_risk"]
        + 0.35 * df_for_map["water_pollution_risk"]
        + 0.25 * df_for_map["flood_risk"]
    )

    fig = px.scatter_mapbox(
        df_for_map,
        lat="latitude",
        lon="longitude",
        color="overall_risk",
        size="population_density",
        color_continuous_scale="RdYlGn_r",
        title="Environmental Risk Map",
        zoom=2,
        mapbox_style="open-street-map",
        opacity=0.7,
        hover_data={
            "latitude": True,
            "longitude": True,
            "air_pollution_risk": True,
            "water_pollution_risk": True,
            "flood_risk": True,
            "overall_risk": True,
        },
    )

    if prediction_point is not None:
        lat, lon = prediction_point
        fig.add_trace(
            go.Scattermapbox(
                lat=[lat],
                lon=[lon],
                mode="markers",
                marker={"size": 18, "color": "red"},
                name="Prediction point",
                text=["Selected location"],
                hoverinfo="text",
            )
        )

    fig.update_layout(
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        width=1000,
        height=500,
    )
    return fig


def build_risk_bar_chart(predictions):
    labels = [
        "Air Pollution",
        "Water Pollution",
        "Flood",
    ]
    values = [
        predictions["air_pollution_risk"]["probability"],
        predictions["water_pollution_risk"]["probability"],
        predictions["flood_risk"]["probability"],
    ]

    fig = go.Figure(
        data=[
            go.Bar(
                x=labels,
                y=values,
                marker={"color": ["#2E8B57", "#F4A300", "#D62828"]},
                text=[f"{v:.2%}" for v in values],
                textposition="outside",
            )
        ]
    )
    fig.update_layout(
        title="Risk Probability by Category",
        xaxis_title="Risk Type",
        yaxis_title="Probability",
        yaxis={"range": [0, 1]},
        height=400,
    )
    return fig

