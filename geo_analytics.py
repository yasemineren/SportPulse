import json
from pathlib import Path


def build_facility_geojson(df):
    features = []
    for _, row in df.iterrows():
        features.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [row["lon"], row["lat"]],
                },
                "properties": {
                    "facility_id": int(row["facility_id"]),
                    "avg_demand": float(row["avg_demand"]),
                },
            }
        )
    return {"type": "FeatureCollection", "features": features}


def export_facility_geojson(df, output_path="sportpulse_facilities.geojson"):
    output_path = Path(output_path)
    geojson = build_facility_geojson(df)
    output_path.write_text(json.dumps(geojson, ensure_ascii=False, indent=2), encoding="utf-8")
    return output_path
