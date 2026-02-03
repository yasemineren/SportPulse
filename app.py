import streamlit as st
import pandas as pd
import plotly.express as px
from model_engine import DemandEngine
from data_gen import generate_sport_data, load_sport_data, save_sport_data
from analytics import (
    load_sql_summary,
    load_weekly_demand_trend,
    load_pricing_insights,
    export_bi_extract,
)
from geo_analytics import export_facility_geojson
from forecast_engine import build_weekly_forecast

# Sayfa Ayarları
st.set_page_config(page_title="SportPulse AI", layout="wide")

st.title("⚡ SportPulse: Akıllı Talep ve Fiyatlama Radarı")

# 1. Veri ve Model Yükleme
@st.cache_resource
def load_system():
    try:
        df = load_sport_data()
    except FileNotFoundError:
        df = generate_sport_data()
        save_sport_data(df)
    engine = DemandEngine()
    engine.train(df)
    return df, engine


@st.cache_data
def load_forecast(df):
    return build_weekly_forecast(df)


df, engine = load_system()
sql_summary = load_sql_summary()
weekly_trend = load_weekly_demand_trend()
pricing_insights = load_pricing_insights()
forecast_history, forecast_outlook, _ = load_forecast(df)
model_metrics = engine.get_metrics()

# 2. Sidebar - Senaryo Oluşturucu
st.sidebar.header("🎛️ Durum Simülasyonu")
input_hour = st.sidebar.slider("Saat", 0, 23, 19)
input_temp = st.sidebar.slider("Sıcaklık (°C)", -5, 40, 25)
input_rain = st.sidebar.checkbox("🌧️ Yağmur Var mı?", value=False)
input_event = st.sidebar.checkbox("🏟️ Yakında Etkinlik Var mı?", value=True)
input_weekend = st.sidebar.checkbox("Hafta Sonu mu?", value=False)
current_price = st.sidebar.number_input("Mevcut Fiyat (TL)", value=150)
distance_to_event = st.sidebar.slider("Etkinliğe Uzaklık (km)", 0.0, 50.0, 12.0, 0.5)

# Girdi verisini DataFrame'e çevir
input_data = pd.DataFrame(
    {
        'hour': [input_hour],
        'is_weekend': [1 if input_weekend else 0],
        'temp': [input_temp],
        'is_rainy': [1 if input_rain else 0],
        'nearby_event': [1 if input_event else 0],
        'distance_to_event': [distance_to_event if input_event else 50.0],
        'price': [current_price],
    }
)

# --- ANA EKRAN ---

col1, col2, col3 = st.columns(3)

# A. Demand Nowcast
predicted_demand = engine.predict_demand(input_data)
occupancy = min(100, (predicted_demand / 100) * 100)  # Kapasite 100 varsayıldı

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

# --- MODEL PERFORMANSI ---

st.divider()

st.subheader("✅ Model Performansı")
metric_cols = st.columns(3)
metric_cols[0].metric("RMSE", f"{model_metrics.get('RMSE', 0):.2f}")
metric_cols[1].metric("MAE", f"{model_metrics.get('MAE', 0):.2f}")
metric_cols[2].metric("Test Örnek Sayısı", f"{model_metrics.get('Test Samples', 0):.0f}")

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
    fig.add_scatter(
        x=[opt_price],
        y=[opt_demand],
        mode='markers',
        marker=dict(size=15, color='green'),
        name='Önerilen',
    )
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("🗺️ Geo Heatmap (Tesis Bazlı)")
    st.info("Tesislerin konumları ve tahmini talep yoğunluğu haritası.")
    facilities = (
        df.groupby(['facility_id', 'lat', 'lon'])['y']
        .mean()
        .reset_index()
        .rename(columns={'y': 'avg_demand'})
    )
    st.map(facilities[['lat', 'lon']])
    st.dataframe(
        facilities.sort_values('avg_demand', ascending=False).head(10),
        use_container_width=True,
    )
    geojson_path = export_facility_geojson(facilities)
    with open(geojson_path, "rb") as geojson_file:
        st.download_button(
            label="🗺️ ArcGIS / GeoJSON indir",
            data=geojson_file,
            file_name=geojson_path.name,
            mime="application/geo+json",
        )

st.divider()

forecast_cols = st.columns([2, 1])
with forecast_cols[0]:
    st.subheader("📈 Haftalık Talep Forecast")
    forecast_chart = px.line(
        forecast_history,
        x="ds",
        y="actual",
        title="Geçmiş Haftalık Ortalama Talep",
    )
    forecast_chart.add_scatter(
        x=forecast_outlook["ds"],
        y=forecast_outlook["forecast"],
        mode="lines",
        name="Forecast",
        line=dict(color="orange"),
    )
    forecast_chart.add_scatter(
        x=forecast_outlook["ds"],
        y=forecast_outlook["lower_ci"],
        mode="lines",
        name="Alt Güven Aralığı",
        line=dict(color="rgba(255,165,0,0.3)", dash="dot"),
    )
    forecast_chart.add_scatter(
        x=forecast_outlook["ds"],
        y=forecast_outlook["upper_ci"],
        mode="lines",
        name="Üst Güven Aralığı",
        line=dict(color="rgba(255,165,0,0.3)", dash="dot"),
    )
    st.plotly_chart(forecast_chart, use_container_width=True)

with forecast_cols[1]:
    st.subheader("📌 Forecast Özeti")
    st.dataframe(
        forecast_outlook.rename(
            columns={
                "ds": "Tarih",
                "forecast": "Forecast",
                "lower_ci": "Alt CI",
                "upper_ci": "Üst CI",
            }
        ),
        use_container_width=True,
    )

st.divider()

st.subheader("🧠 Gelişmiş SQL İçgörüleri (Window + Join)")
st.dataframe(pricing_insights.head(20), use_container_width=True)

st.subheader("🗄️ SQL Analiz Özeti (Power BI / Tableau için hazır)")
st.dataframe(sql_summary, use_container_width=True)
trend_fig = px.line(
    weekly_trend,
    x="week_of_year",
    y="avg_demand",
    title="Haftalık Ortalama Talep Trendi (SQL)",
)
st.plotly_chart(trend_fig, use_container_width=True)

bi_extract_path = export_bi_extract(sql_summary)
with open(bi_extract_path, "rb") as data_file:
    st.download_button(
        label="📥 BI Extract (CSV) indir",
        data=data_file,
        file_name=bi_extract_path.name,
        mime="text/csv",
    )
