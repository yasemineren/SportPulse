# SportPulse
# ⚡ SportPulse: AI-Driven Demand & Dynamic Pricing Engine

> **"Sadece tahmin etme, yönet."** — Hava durumu, etkinlikler ve fiyat duyarlılığını analiz ederek spor tesisleri için dinamik talep tahmini ve gelir optimizasyonu yapan yapay zeka motoru.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red)
![XGBoost](https://img.shields.io/badge/Model-XGBoost-green)
![SHAP](https://img.shields.io/badge/XAI-SHAP-orange)

## 🎯 Projenin Amacı
Spor tesisleri ve aktivite alanları için talep sadece fiyata bağlı değildir. Yağmur, hafta sonu tatilleri, yakındaki bir futbol maçı veya trafik durumu talebi anlık olarak değiştirebilir. 

**SportPulse**, bu dış faktörleri simüle ederek:
1.  **Gelecek Talebi Tahmin Eder (Nowcasting):** Önümüzdeki saatlerde doluluk ne olacak?
2.  **Dinamik Fiyat Önerir:** Geliri (Revenue) maksimize eden en doğru fiyat nedir?
3.  **Nedenini Açıklar (XAI):** "Talep neden düştü?" sorusuna *"Çünkü yağmur başladı ve fiyat çok yüksek"* gibi açıklanabilir yanıtlar verir.

## 🏗️ Mimari ve Özellikler

Bu proje 4 ana modülden oluşur:

### 1. Demand Shock Detector (Talep Şoku Dedektörü) 🚨
Model, normalden sapan talep hareketlerini algılar ve **SHAP** değerlerini kullanarak sebebini açıklar.
* *Örnek:* "Bugün talep beklenenden %40 yüksek. Sebep: Yakındaki Konser Etkinliği (+25 Etki Puanı)."

### 2. Dynamic Pricing Optimizer (Fiyat Optimizasyonu) 💰
**SciPy** ve simülasyon teknikleri kullanarak, doluluğu ve birim fiyatı dengeleyen optimum noktayı bulur.
* *Çıktı:* "Mevcut fiyat 150 TL yerine 180 TL yapılırsa, doluluk %5 düşecek ama toplam ciro %12 artacak."

### 3. Sensitivity Lab (Duyarlılık Laboratuvarı) 🌡️
Havanın, günün saatinin veya özel günlerin talebi nasıl etkilediğini analiz eden interaktif simülasyon ortamı.
### 4. Geo Analytics & SQL Pipeline 🗺️🗄️
Tesis koordinatları, etkinlik uzaklığı ve SQL veri akışı sayesinde bölgesel talep farklarını analiz eder.
* *Çıktı:* Tesis bazlı ortalama talep yoğunluğu tablosu ve harita görünümü.
* *BI Hazır Çıktı:* Power BI / Tableau için CSV extract.
* *ArcGIS/GeoJSON:* Tesis verilerinin GeoJSON çıktısı.

## 🚀 Kurulum ve Çalıştırma

Proje yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin:

1.  **Repoyu klonlayın:**
    ```bash
    git clone [https://github.com/KULLANICI_ADIN/SportPulse.git](https://github.com/KULLANICI_ADIN/SportPulse.git)
    cd SportPulse
    ```

2.  **Gerekli kütüphaneleri yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Uygulamayı başlatın:**
    ```bash
    streamlit run app.py
    ```

## 📂 Dosya Yapısı

* `analytics.py`: SQL sorguları, haftalık trend analizi ve BI için CSV export yardımcıları.
* `geo_analytics.py`: GeoJSON üretimi ve ArcGIS uyumlu çıktı hazırlığı.
* `data_gen.py`: Mevsimsellik, hava durumu ve etkinlik verilerini içeren gelişmiş sentetik veri üreticisi.
    * SQLite veri yazma/okuma akışı (`sportpulse.db`) ve etkinlik uzaklığı hesaplaması içerir.
* `model_engine.py`: XGBoost model eğitimi, SHAP analizi ve fiyat optimizasyon algoritmalarını içeren çekirdek motor.
* `app.py`: Streamlit tabanlı interaktif dashboard arayüzü.
    * SQL üzerinden veri yükleme ve tesis bazlı harita analizi yapılır.
* `requirements.txt`: Tek komutla kurulum için bağımlılık listesi.
* `Makefile`: `make setup`, `make data`, `make run` ile tekrar üretilebilir çalışma akışı.
* `r_scripts/sql_summary.R`: R ile SQL özet çıktısı (DBI/RSQLite).
* `reports/bi_mockup.md`: Power BI / Tableau mockup taslağı.

## 📸 Ekran Görüntüleri (Örnek)

*(Buraya projenin çalışırken aldığı bir ekran görüntüsünü eklersen harika olur)*

## 🔮 Gelecek Planları
* [ ] Gerçek zamanlı hava durumu API entegrasyonu (OpenWeatherMap).
* [ ] Rakip fiyat analizi modülü.
* [ ] CRM entegrasyonu ile kişiye özel fiyat teklifleri.

---
*Developed by [Yasemin EREN] - 2026*
