import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX


def prepare_weekly_series(df):
    weekly = df.copy()
    weekly["ds"] = pd.to_datetime(weekly["ds"])
    weekly = (
        weekly.resample("W-MON", on="ds")["y"]
        .mean()
        .reset_index()
        .sort_values("ds")
    )
    return weekly


def build_weekly_forecast(df, periods=8):
    weekly = prepare_weekly_series(df)
    series = weekly.set_index("ds")["y"]

    model = SARIMAX(
        series,
        order=(1, 1, 1),
        seasonal_order=(1, 0, 1, 52),
        enforce_stationarity=False,
        enforce_invertibility=False,
    )
    results = model.fit(disp=False)

    forecast = results.get_forecast(steps=periods)
    predicted = forecast.predicted_mean
    conf_int = forecast.conf_int()

    forecast_df = pd.DataFrame(
        {
            "ds": predicted.index,
            "forecast": predicted.values,
            "lower_ci": conf_int.iloc[:, 0].values,
            "upper_ci": conf_int.iloc[:, 1].values,
        }
    )
    history = weekly.rename(columns={"y": "actual"})
    return history, forecast_df, results
