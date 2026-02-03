# SportPulse ↔︎ Data Scientist Pozisyonu Uyum Analizi

Bu doküman, SportPulse projesinin ilan edilen Data Scientist rolü ile ne kadar örtüştüğünü değerlendirir ve eksik görülen alanları kapatmak için proje içinde yapılan tamamlamaları özetler.

## 1) Rol Özeti (İlandan)
- Spor ve fiziksel aktivite sektörüne yönelik **talep / arz modelleme**, **optimum fiyatlama**, **duyarlılık analizi** ve **tahminleme**.
- Büyük ve karmaşık verilerde **ML/AI** tabanlı içgörü çıkarımı.
- **Paydaş iletişimi** ve stratejik karar desteği.

## 2) SportPulse ile Uyum Noktaları

### ✅ Temel Gereksinimler
- **3+ yıl veri bilimi / analitik deneyim**: Proje kapsamı iş tecrübesini doğrulamaz; ancak portföy düzeyinde ileri modelleme, optimizasyon ve açıklanabilirlik bileşenlerini içerir.
- **Python / R / SQL yetkinliği**:
  - Python: XGBoost, SHAP, Streamlit, SciPy, statsmodels.
  - R: `r_scripts/sql_summary.R` ile SQL özetleme.
  - SQL: SQLite pipeline ve window fonksiyonlu raporlama.

### ✅ Rolün Teknik Odağı ile Örtüşen Modüller
- **Talep modelleme**: `model_engine.py` (XGBoost + SHAP).
- **Optimum fiyatlama**: `model_engine.py` fiyat optimizasyonu.
- **Duyarlılık analizi**: Streamlit üzerinde fiyat esnekliği simülasyonu.
- **Tahminleme / forecasting**: `forecast_engine.py` (SARIMAX).
- **Coğrafi analiz**: `geo_analytics.py` + GeoJSON export.
- **BI çıktıları**: CSV extract + Power BI / Tableau mockup.

## 3) Desirable Yetkinlikler ile Eşleşme
- **Geospatial & ArcGIS**: GeoJSON export ile ArcGIS uyumu mevcut.
- **Power BI / Tableau**: CSV extract ve mockup dokümanı mevcut.
- **Stakeholder-facing / danışmanlık**: README içinde akış ve KPI anlatımı mevcut.
- **Reproducible workflows & Git**: Makefile ve modüler yapı mevcut.
- **İnovasyon**: Roadmap içinde API entegrasyonları ve ileri modüller bulunuyor.

## 4) Eksikler ve Tamamlama Adımları

### 4.1 Eksik / Zayıf Alanlar
- **Arz (supply) modelleme**: Proje ağırlıklı olarak talep tarafında.
- **Kapasite / doluluk ölçümü**: Talep metrikleri var, kapasite tarafı açık.
- **Kurumsal raporlama paketi**: BI mockup var, ancak tam bir “supply–demand” özet tablosu yok.

### 4.2 Bu Eksikleri Kapatmak İçin Eklenenler
- **Arz-talep dengesi yardımcı analizleri**: `supply_demand.py`
  - Tesis bazlı kapasite, ortalama doluluk ve kapasite açığı gibi metrikler.
  - Arz-talep dengesini raporlanabilir hale getirir.

### 4.3 Eklenebilecek (Opsiyonel) Geliştirmeler
- **Gerçek kapasite kaynakları** (CRM/rezervasyon sistemi) ile entegrasyon.
- **Fiyat esnekliği kalibrasyonu** için gerçek müşteri verisi.
- **BI dashboard** için örnek Power BI / Tableau dosyası paylaşımı.

## 5) Sonuç
SportPulse, ilandaki rolün çekirdek teknik gereksinimlerine güçlü şekilde karşılık verir. Eklenen arz-talep denge modülü, özellikle “supply modelling” başlığındaki eksikliği kapatmak için uygulanabilir bir temel sağlar. Bu haliyle proje, rol için **uygun ve ikna edici bir portföy** niteliğindedir.
