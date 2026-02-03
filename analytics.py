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


def load_pricing_insights(db_path=DB_PATH):
    db_path = Path(db_path)
    if not db_path.exists():
        raise FileNotFoundError(f"Database not found: {db_path}")
    with sqlite3.connect(db_path) as conn:
        query = """
            WITH base AS (
                SELECT
                    facility_id,
                    DATE(ds) AS day,
                    STRFTIME('%W', ds) AS week_of_year,
                    price,
                    y,
                    is_weekend
                FROM sport_data
            ),
            facility_stats AS (
                SELECT
                    facility_id,
                    COUNT(*) AS facility_obs,
                    ROUND(AVG(price), 2) AS facility_avg_price,
                    ROUND(AVG(y), 2) AS facility_avg_demand
                FROM base
                GROUP BY facility_id
            ),
            weekly AS (
                SELECT
                    facility_id,
                    week_of_year,
                    ROUND(AVG(price), 2) AS avg_price,
                    ROUND(AVG(y), 2) AS avg_demand,
                    ROUND(AVG(CASE WHEN is_weekend = 1 THEN y END), 2) AS weekend_avg_demand
                FROM base
                GROUP BY facility_id, week_of_year
            ),
            ranked AS (
                SELECT
                    facility_id,
                    week_of_year,
                    avg_price,
                    avg_demand,
                    weekend_avg_demand,
                    RANK() OVER (PARTITION BY week_of_year ORDER BY avg_demand DESC) AS demand_rank,
                    AVG(avg_price) OVER (
                        PARTITION BY facility_id
                        ORDER BY CAST(week_of_year AS INTEGER)
                        ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
                    ) AS price_ma_4w,
                    LAG(avg_price) OVER (
                        PARTITION BY facility_id
                        ORDER BY CAST(week_of_year AS INTEGER)
                    ) AS prev_week_price
                FROM weekly
            )
            SELECT
                ranked.facility_id,
                ranked.week_of_year,
                ranked.avg_price,
                ranked.avg_demand,
                ranked.weekend_avg_demand,
                ranked.demand_rank,
                ROUND(ranked.price_ma_4w, 2) AS price_ma_4w,
                ROUND(ranked.prev_week_price, 2) AS prev_week_price,
                facility_stats.facility_obs,
                facility_stats.facility_avg_price,
                facility_stats.facility_avg_demand
            FROM ranked
            JOIN facility_stats ON facility_stats.facility_id = ranked.facility_id
            ORDER BY CAST(ranked.week_of_year AS INTEGER), ranked.demand_rank
        """
        return pd.read_sql_query(query, conn)


def export_bi_extract(df, output_path="sportpulse_bi_extract.csv"):
    output_path = Path(output_path)
    df.to_csv(output_path, index=False)
    return output_path
