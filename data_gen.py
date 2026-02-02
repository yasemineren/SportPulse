import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sport_data(days=365):
    dates = pd.date_range(start="2024-01-01", periods=days*24, freq="H")
    data = []

    for date in dates:
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
        demand -= is_rainy * 40            # Yağmur düşürür (Açık saha varsayımı)
        demand -= (price - 100) * 0.5      # Fiyat arttıkça talep düşer (Fiyat Esnekliği)
        demand += np.random.normal(0, 5)   # Gürültü
        
        # Negatif talep olamaz, kapasite max 100
        demand = max(0, min(100, demand))
        
        data.append([date, hour, is_weekend, temp, is_rainy, nearby_event, price, demand])

    df = pd.DataFrame(data, columns=['ds', 'hour', 'is_weekend', 'temp', 'is_rainy', 'nearby_event', 'price', 'y'])
    return df

# Veriyi kaydet
df = generate_sport_data()
df.to_csv("sportpulse_data.csv", index=False)
print("Veri seti oluşturuldu: sportpulse_data.csv")
