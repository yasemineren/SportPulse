import pandas as pd


DEFAULT_CAPACITY_BY_FACILITY = {
    1: 90,
    2: 100,
    3: 110,
    4: 95,
    5: 105,
    6: 120,
    7: 85,
    8: 115,
}


def add_capacity(df, capacity_by_facility=None, default_capacity=100):
    capacity_by_facility = capacity_by_facility or DEFAULT_CAPACITY_BY_FACILITY
    enriched = df.copy()
    if "capacity" not in enriched.columns:
        enriched["capacity"] = enriched["facility_id"].map(capacity_by_facility).fillna(default_capacity)
    return enriched


def build_supply_demand_summary(df):
    enriched = add_capacity(df)
    enriched["utilization"] = (enriched["y"] / enriched["capacity"]).clip(0, 1)
    enriched["capacity_gap"] = (enriched["capacity"] - enriched["y"]).clip(lower=0)

    facility_summary = (
        enriched.groupby("facility_id", as_index=False)
        .agg(
            avg_capacity=("capacity", "mean"),
            avg_demand=("y", "mean"),
            avg_utilization=("utilization", "mean"),
            avg_capacity_gap=("capacity_gap", "mean"),
        )
        .sort_values("avg_utilization", ascending=False)
    )

    overall_summary = pd.DataFrame(
        {
            "avg_capacity": [enriched["capacity"].mean()],
            "avg_demand": [enriched["y"].mean()],
            "avg_utilization": [enriched["utilization"].mean()],
            "avg_capacity_gap": [enriched["capacity_gap"].mean()],
        }
    )

    return facility_summary, overall_summary
