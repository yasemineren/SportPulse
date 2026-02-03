import sqlite3
from pathlib import Path

import pandas as pd

DB_PATH = Path("sportpulse.db")


def load_sql_summary(db_path=DB_PATH):
    db_path = Path(db_path)
    if not db_path.exists():
        raise FileNotFoundError(f"Database not found: {db_path}")
    with sqlite3.connect(db_path) as conn:
        query = """
            SELECT
                facility_id,
                ROUND(AVG(y), 2) AS avg_demand,
                ROUND(AVG(price), 2) AS avg_price,
                ROUND(AVG(distance_to_event), 2) AS avg_event_distance,
                COUNT(*) AS obs_count
            FROM sport_data
            GROUP BY facility_id
            ORDER BY avg_demand DESC
        """
        return pd.read_sql_query(query, conn)


def load_weekly_demand_trend(db_path=DB_PATH):
    db_path = Path(db_path)
    if not db_path.exists():
        raise FileNotFoundError(f"Database not found: {db_path}")
    with sqlite3.connect(db_path) as conn:
        query = """
            SELECT
                STRFTIME('%W', ds) AS week_of_year,
                ROUND(AVG(y), 2) AS avg_demand,
                ROUND(AVG(price), 2) AS avg_price
            FROM sport_data
            GROUP BY week_of_year
            ORDER BY CAST(week_of_year AS INTEGER)
        """
        return pd.read_sql_query(query, conn)


def export_bi_extract(df, output_path="sportpulse_bi_extract.csv"):
    output_path = Path(output_path)
    df.to_csv(output_path, index=False)
    return output_path
