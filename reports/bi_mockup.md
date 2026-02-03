# Power BI / Tableau Mockup

Bu doküman, SportPulse için örnek bir BI rapor mockup'ını tarif eder.

## Sayfa 1: Executive Overview
- KPI kartları: Ortalama Talep, Ortalama Fiyat, Ortalama Etkinlik Uzaklığı, Toplam Gözlem.
- Çizgi grafik: Haftalık Ortalama Talep Trendi.
- Harita: Tesis lokasyonları ve ortalama talep (GeoJSON ile).

## Sayfa 2: Facility Drilldown
- Tablo: Facility ID, Avg Demand, Avg Price, Avg Event Distance, Obs Count.
- Slicer: Facility ID / Week of Year.

## Veri Kaynakları
- `sportpulse_bi_extract.csv` (Python/Streamlit export)
- `sportpulse_sql_summary_r.csv` (R script export)
- `sportpulse_facilities.geojson` (ArcGIS/GeoJSON export)

## Notlar
- Bu mockup, Power BI veya Tableau’da hızlıca uygulanabilecek bir sayfa düzeni önerisidir.
