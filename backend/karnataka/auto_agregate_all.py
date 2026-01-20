import os
import pandas as pd

BASE_DIR = "."

for folder in os.listdir(BASE_DIR):
    folder_path = os.path.join(BASE_DIR, folder)

    if os.path.isdir(folder_path):
        for file in os.listdir(folder_path):
            if file.endswith("_clean.csv"):
                clean_path = os.path.join(folder_path, file)
                daily_path = clean_path.replace("_clean.csv", "_daily_price.csv")

                if os.path.exists(daily_path):
                    continue

                df = pd.read_csv(clean_path)
                df["date"] = pd.to_datetime(df["date"])

                daily = (
                    df.groupby("date")["modal_price"]
                    .mean()
                    .reset_index()
                    .rename(columns={"modal_price": "avg_modal_price"})
                )

                daily.sort_values("date").to_csv(daily_path, index=False)
                print(f"📊 Daily series created for {file}")
