import pandas as pd
import sys

if len(sys.argv) < 2:
    print("❌ Usage: python test_single_commodity.py <commodity_name>")
    sys.exit(1)

commodity_name = sys.argv[1].lower()

df = pd.read_csv("final_price_forecast_summary.csv")
result = df[df["Commodity"] == commodity_name]

if result.empty:
    print(f"❌ No forecast available for {commodity_name}")
else:
    print(f"\n📊 PRICE ADVISORY FOR {commodity_name.upper()}")
    print(result.to_string(index=False))
