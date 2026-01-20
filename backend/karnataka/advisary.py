import pandas as pd
import sys

STATE = "Karnataka"
SUMMARY_FILE = "final_price_forecast_summary.csv"


def get_advisory_data(commodity_input):
    commodity_input = commodity_input.lower()

    # ---------- LOAD SUMMARY ----------
    df = pd.read_csv(SUMMARY_FILE)

    row = df[df["Commodity"] == commodity_input]

    if row.empty:
        raise ValueError(f"No advisory available for '{commodity_input}'")

    row = row.iloc[0]

    # ---------- EXTRACT VALUES ----------
    commodity = row["Commodity"].upper()
    action = row["Action"]
    days = int(row["Store_Days"])
    expected_price = float(row["Expected_Price"])
    profit = float(row["Profit_per_Quintal"])
    confidence = row["Confidence"]

    # Today price calculation
    today_price = round(expected_price - profit, 2)

    # Generic price range (safe fallback)
    low_price = round(expected_price * 0.9, 2)
    high_price = round(expected_price * 1.1, 2)

    emoji = "🍅" if commodity == "TOMATO" else "🌾"

    return {
        "state": STATE,
        "commodity": commodity,
        "emoji": emoji,
        "today_price": today_price,
        "recommendation": action,
        "store_days": days,
        "expected_price": round(expected_price, 2),
        "price_range_low": low_price,
        "price_range_high": high_price,
        "extra_profit": round(profit, 2),
        "confidence": confidence
    }


# ---------- CLI SUPPORT (UNCHANGED FOR YOU) ----------
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("❌ Usage: python advisary.py <commodity_name>")
        sys.exit(1)

    commodity_input = sys.argv[1]

    try:
        data = get_advisory_data(commodity_input)

        print(f"""
{data['emoji']} {data['commodity']} PRICE ADVISORY ({data['state'].upper()})
📅 Today Price: ₹{data['today_price']} / quintal

{'✅' if data['recommendation'] == 'STORE' else '❌'} RECOMMENDATION: {data['recommendation']}
🕒 Duration       : {data['store_days']} days
📈 Expected Price : ₹{data['expected_price']}
📊 Price Range    : ₹{data['price_range_low']} – {data['price_range_high']}
💰 Extra Profit   : ₹{data['extra_profit']} / quintal

🔍 Confidence Level: {data['confidence']}
""")

    except Exception as e:
        print(f"❌ {e}")
