import os
import pandas as pd
from prophet import Prophet

# ================= CONFIG =================
BASE_DIR = "."   # run inside karnataka folder
DEFAULT_STORAGE_COST = 10
DEFAULT_FORECAST_DAYS = 15

STORAGE_CONFIG = {
    "tomato": {"cost": 20, "days": 15},
    "onion": {"cost": 8,  "days": 30},
    "potato": {"cost": 6, "days": 30},
    "brinjal": {"cost": 15, "days": 15},
    "cabbage": {"cost": 10, "days": 20},
}

# =========================================

def get_config(commodity):
    return STORAGE_CONFIG.get(
        commodity.lower(),
        {"cost": DEFAULT_STORAGE_COST, "days": DEFAULT_FORECAST_DAYS}
    )

summary = []

for folder in os.listdir(BASE_DIR):
    folder_path = os.path.join(BASE_DIR, folder)

    if not os.path.isdir(folder_path):
        continue

    for file in os.listdir(folder_path):
        if not file.endswith("_daily_price.csv"):
            continue

        commodity = file.replace("_daily_price.csv", "")
        file_path = os.path.join(folder_path, file)

        df = pd.read_csv(file_path)

        # Rename for Prophet
        df.columns = ["ds", "y"]

        # -------- SAFETY CHECK --------
        if len(df.dropna()) < 2:
            print(f"⚠️ Skipped {commodity}: insufficient data")
            continue

        config = get_config(commodity)
        storage_cost = config["cost"]
        forecast_days = config["days"]

        # -------- MODEL --------
        model = Prophet(
            weekly_seasonality=True,
            yearly_seasonality=False
        )

        model.fit(df)

        # -------- FORECAST --------
        future = model.make_future_dataframe(periods=forecast_days)
        forecast = model.predict(future)

        future_prices = forecast[
            ["ds", "yhat", "yhat_lower", "yhat_upper"]
        ].tail(forecast_days)

        today_price = df.iloc[-1]["y"]
        today_date = pd.to_datetime(df.iloc[-1]["ds"])

        best_decision = {
            "Action": "SELL NOW",
            "Store_Days": 0,
            "Expected_Price": round(today_price, 2),
            "Profit_per_Quintal": 0,
            "Confidence": "LOW"
        }

        # -------- DECISION LOGIC --------
        for _, row in future_prices.iterrows():
            days = (row["ds"] - today_date).days
            profit = row["yhat"] - today_price - (storage_cost * days)

            if profit > best_decision["Profit_per_Quintal"]:
                spread = row["yhat_upper"] - row["yhat_lower"]
                confidence = "HIGH" if spread < 600 else "MEDIUM"

                best_decision = {
                    "Action": "STORE",
                    "Store_Days": days,
                    "Expected_Price": round(row["yhat"], 2),
                    "Profit_per_Quintal": round(profit, 2),
                    "Confidence": confidence
                }

        summary.append({
            "Commodity": commodity,
            **best_decision
        })

        print(f"✅ Forecast completed for {commodity}")

# -------- SAVE FINAL SUMMARY --------
summary_df = pd.DataFrame(summary)
summary_df.to_csv("final_price_forecast_summary.csv", index=False)

print("\n🎉 FINAL FORECAST READY")
print(summary_df)
