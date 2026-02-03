import pandas as pd
import xgboost as xgb
import shap
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error


class DemandEngine:
    def __init__(self):
        self.model = None
        self.explainer = None
        self.metrics = {}

    def train(self, df):
        # Özellikler ve Hedef
        X = df[
            [
                'hour',
                'is_weekend',
                'temp',
                'is_rainy',
                'nearby_event',
                'distance_to_event',
                'price',
            ]
        ]
        y = df['y']

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Modeli Eğit
        self.model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100)
        self.model.fit(X_train, y_train)

        # Model metrikleri
        predictions = self.model.predict(X_test)
        rmse = mean_squared_error(y_test, predictions, squared=False)
        mae = mean_absolute_error(y_test, predictions)
        self.metrics = {
            "RMSE": rmse,
            "MAE": mae,
            "Test Samples": len(y_test),
        }

        # SHAP Explainer (Shock Detector için)
        self.explainer = shap.Explainer(self.model)

        return self.model

    def predict_demand(self, features):
        # features: DataFrame tek satır
        pred = self.model.predict(features)[0]
        return max(0, pred)

    def get_metrics(self):
        return self.metrics

    def get_shock_reason(self, features):
        """
        Demand Shock Detector:
        Tahmini en çok artıran veya azaltan faktörü bulur.
        """
        shap_values = self.explainer(features)

        # En büyük etkiyi yaratan faktörü bul
        values = shap_values.values[0]
        feature_names = features.columns

        max_impact_idx = abs(values).argmax()
        impact_feature = feature_names[max_impact_idx]
        impact_value = values[max_impact_idx]

        direction = "ARTIRAN" if impact_value > 0 else "DÜŞÜREN"

        explanation = (
            f"Talep üzerinde en büyük etki: **{impact_feature}**. Durumu **{direction}** yönde "
            f"etkiliyor (Etki Skoru: {impact_value:.2f})."
        )

        if impact_feature == 'is_rainy' and impact_value < 0:
            explanation += " 🌧️ Yağmur nedeniyle açık hava rezervasyonlarında ciddi düşüş var."
        elif impact_feature == 'nearby_event' and impact_value > 0:
            explanation += " 🏟️ Yakındaki maç/konser nedeniyle talep patlaması!"

        return explanation

    def optimize_price(self, features_base):
        """
        Dinamik Fiyatlama: Geliri (Fiyat x Talep) maksimize eden fiyatı bul.
        """
        best_price = features_base['price'].iloc[0]
        max_revenue = 0
        best_demand = 0

        # 50 TL ile 300 TL arasında simülasyon yap
        for p in range(50, 301, 10):
            temp_df = features_base.copy()
            temp_df['price'] = p
            demand = self.predict_demand(temp_df)
            revenue = p * demand

            if revenue > max_revenue:
                max_revenue = revenue
                best_price = p
                best_demand = demand

        return best_price, best_demand, max_revenue
