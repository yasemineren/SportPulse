import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

DB_PATH = Path("sportpulse.db")

def haversine_km(lat1, lon1, lat2, lon2):
    """Calculate distance between two lat/lon pairs in kilometers."""
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    return 6371 * c

def generate_sport_data(days=365, facilities=8):
    dates = pd.date_range(start="2024-01-01", periods=days*24, freq="H")
    data = []

    base_lat, base_lon = 39.93, 32.85
    facility_coords = [
        (
            idx,
            base_lat + np.random.randn() / 200,
            base_lon + np.random.randn() / 200,
        )
        for idx in range(1, facilities + 1)
    ]

    for date in dates:
        facility_id, facility_lat, facility_lon = facility_coords[np.random.randint(0, facilities)]
        # 1. Temel Faktörler
        hour = date.hour
        month = date.month
        is_weekend = 1 if date.weekday() >= 5 else 0
        
        # 2. Dış Faktörler (Simüle Edilmiş)
        # Yağmur ihtimali kışın artar
        rain_prob = 0.8 if month in [12, 1, 2] else 0.2
        is_rainy = 1 if np.random.rand() < rain_prob and np.random.rand() < 0.3 else 0
        
        # Etkinlik (Maç günü vb.) - Rastgele %5 ihtimal
        nearby_event = 1 if np.random.rand() < 0.05 else 0
        event_lat = base_lat + np.random.randn() / 100
        event_lon = base_lon + np.random.randn() / 100
        distance_to_event = (
            haversine_km(facility_lat, facility_lon, event_lat, event_lon)
            if nearby_event
            else 50.0
        )
        
        # Sıcaklık (Mevsimsel + Rastgelelik)
        base_temp = 25 - abs(month - 7) * 3
        temp = base_temp + np.random.normal(0, 3) - (is_rainy * 5)

        # 3. Fiyatlandırma (Dinamik fiyat simülasyonu)
        # Akşam saatleri (18-22) prime time
        is_prime_time = 1 if 18 <= hour <= 22 else 0
        base_price = 100
        price = base_price + (is_prime_time * 50) + (is_weekend * 20)
        
        # 4. TALEP OLUŞTURMA (Ground Truth Logic)
        # Baz talep
        demand = 20 
        
        # Etkiler
        demand += is_prime_time * 30       # Akşam saati artırır
        demand += is_weekend * 15          # Haftasonu artırır
        demand += nearby_event * 25        # Yakın etkinlik artırır
        demand += max(0, (30 - distance_to_event)) * 0.8
        demand -= is_rainy * 40            # Yağmur düşürür (Açık saha varsayımı)
        demand -= (price - 100) * 0.5      # Fiyat arttıkça talep düşer (Fiyat Esnekliği)
        demand += np.random.normal(0, 5)   # Gürültü
        
        # Negatif talep olamaz, kapasite max 100
        demand = max(0, min(100, demand))
        
        data.append([
            date,
            facility_id,
            facility_lat,
            facility_lon,
            hour,
            is_weekend,
            temp,
            is_rainy,
            nearby_event,
            distance_to_event,
            price,
            demand,
        ])

    df = pd.DataFrame(
        data,
        columns=[
            'ds',
            'facility_id',
            'lat',
            'lon',
            'hour',
            'is_weekend',
            'temp',
            'is_rainy',
            'nearby_event',
            'distance_to_event',
            'price',
            'y',
        ],
    )
    return df

def save_sport_data(df, db_path=DB_PATH):
    db_path = Path(db_path)
    with sqlite3.connect(db_path) as conn:
        df.to_sql("sport_data", conn, if_exists="replace", index=False)


def load_sport_data(db_path=DB_PATH):
    db_path = Path(db_path)
    if not db_path.exists():
        raise FileNotFoundError(f"Database not found: {db_path}")
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query("SELECT * FROM sport_data", conn)


if __name__ == "__main__":
    df = generate_sport_data()
    df.to_csv("sportpulse_data.csv", index=False)
    save_sport_data(df)
    print("Veri seti oluşturuldu: sportpulse_data.csv ve sportpulse.db")
