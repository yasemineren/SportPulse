import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from model_engine import DemandEngine
from data_gen import generate_sport_data

# Sayfa Ayarları
st.set_page_config(page_title="SportPulse AI", layout="wide")

st.title("⚡ SportPulse: Akıllı Talep ve Fiyatlama Radarı")

# 1. Veri ve Model Yükleme
@st.cache_resource
def load_system():
    df = generate_sport_data()
    engine = DemandEngine()
    engine.train(df)
    return df, engine

df, engine = load_system()

# 2. Sidebar - Senaryo Oluşturucu
st.sidebar.header("🎛️ Durum Simülasyonu")
input_hour = st.sidebar.slider("Saat", 0, 23, 19)
input_temp = st.sidebar.slider("Sıcaklık (°C)", -5, 40, 25)
input_rain = st.sidebar.checkbox("🌧️ Yağmur Var mı?", value=False)
input_event = st.sidebar.checkbox("🏟️ Yakında Etkinlik Var mı?", value=True)
input_weekend = st.sidebar.checkbox("Hafta Sonu mu?", value=False)
current_price = st.sidebar.number_input("Mevcut Fiyat (TL)", value=150)

# Girdi verisini DataFrame'e çevir
input_data = pd.DataFrame({
    'hour': [input_hour],
    'is_weekend': [1 if input_weekend else 0],
    'temp': [input_temp],
    'is_rainy': [1 if input_rain else 0],
    'nearby_event': [1 if input_event else 0],
    'price': [current_price]
})

# --- ANA EKRAN ---

col1, col2, col3 = st.columns(3)

# A. Demand Nowcast
predicted_demand = engine.predict_demand(input_data)
occupancy = min(100, (predicted_demand / 100) * 100) # Kapasite 100 varsayıldı

with col1:
    st.subheader("📊 Demand Nowcast")
    st.metric(label="Tahmini Doluluk", value=f"%{occupancy:.1f}", delta=f"{predicted_demand:.0f} Kişi")
    st.progress(float(occupancy) / 100)

# B. Demand Shock Detector (TWIST)
with col2:
    st.subheader("🚨 Shock Detector")
    explanation = engine.get_shock_reason(input_data)
    
    if "ARTIRAN" in explanation:
        st.success(explanation)
    else:
        st.error(explanation)

# C. Dynamic Pricing
with col3:
    st.subheader("💰 Fiyat Önerisi")
    opt_price, opt_demand, opt_rev = engine.optimize_price(input_data)
    
    current_rev = current_price * predicted_demand
    uplift = ((opt_rev - current_rev) / current_rev) * 100 if current_rev > 0 else 0
    
    st.metric(label="Önerilen Fiyat", value=f"{opt_price} TL", delta=f"%{uplift:.1f} Gelir Artışı")
    st.write(f"Tahmini Gelir: **{opt_rev:.0f} TL** (Mevcut: {current_rev:.0f} TL)")

# --- DETAYLI ANALİZLER ---

st.divider()

c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("🌡️ Sensitivity Lab (Hava ve Fiyat Etkisi)")
    # Fiyat esnekliği grafiği oluştur
    prices = range(50, 300, 10)
    demands = []
    for p in prices:
        temp_in = input_data.copy()
        temp_in['price'] = p
        demands.append(engine.predict_demand(temp_in))
    
    chart_data = pd.DataFrame({'Fiyat': prices, 'Tahmini Talep': demands})
    fig = px.line(chart_data, x='Fiyat', y='Tahmini Talep', title="Fiyat Esneklik Eğrisi (Mevcut Koşullarda)")
    # Optimum noktayı işaretle
    fig.add_scatter(x=[opt_price], y=[opt_demand], mode='markers', marker=dict(size=15, color='green'), name='Önerilen')
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("🗺️ Geo Heatmap (Simüle)")
    st.info("Bu bölgedeki tesisler için talep yoğunluğu haritası.")
    # Fake koordinat verisi
    map_data = pd.DataFrame(
        np.random.randn(50, 2) / [50, 50] + [39.93, 32.85], # Ankara koordinatları
        columns=['lat', 'lon'])
    st.map(map_data)
