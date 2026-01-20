import os
import pandas as pd

BASE_DIR = "."

def clean_commodity(raw_path, clean_path):
    clean_rows = []
    current_market = None

    with open(raw_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if line.startswith("Market Name"):
                current_market = line.replace("Market Name :", "").strip()
                continue

            if (
                not line
                or line.startswith("Arrival Date")
                or line.startswith("Commodity")
                or line.startswith("Date Wise")
            ):
                continue

            parts = line.split(",")

            if len(parts) >= 6 and current_market:
                clean_rows.append([
                    parts[0],
                    current_market,
                    parts[1],
                    parts[5]
                ])

    df = pd.DataFrame(
        clean_rows,
        columns=["date", "market", "arrival", "modal_price"]
    )

    df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
    df["arrival"] = pd.to_numeric(df["arrival"], errors="coerce")
    df["modal_price"] = pd.to_numeric(df["modal_price"], errors="coerce")

    df.dropna().to_csv(clean_path, index=False)

# -------- LOOP THROUGH ALL COMMODITIES --------
for folder in os.listdir(BASE_DIR):
    folder_path = os.path.join(BASE_DIR, folder)

    if os.path.isdir(folder_path):
        for file in os.listdir(folder_path):
            if file.endswith(".csv") and not file.endswith("_clean.csv"):
                raw_file = os.path.join(folder_path, file)
                name = file.replace(".csv", "")
                clean_file = os.path.join(folder_path, f"{name}_clean.csv")

                if not os.path.exists(clean_file):
                    clean_commodity(raw_file, clean_file)
                    print(f"✅ Cleaned: {file}")
