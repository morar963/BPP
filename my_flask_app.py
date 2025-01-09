from flask import Flask, jsonify
import requests
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# List of coins
coins = ["BTC", "ETH", "USDT", "DOGE", "TON", "SHIB"]

# Function to get detailed coin data
def get_coin_data(coin):
    url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={coin}USDT"
    response = requests.get(url)
    try:
        data = response.json()
        return {
            "coin": data.get("symbol", f"{coin}USDT"),
            "priceChange": data.get("priceChange"),
            "priceChangePercent": data.get("priceChangePercent"),
            "weightedAvgPrice": data.get("weightedAvgPrice"),
            "prevClosePrice": data.get("prevClosePrice"),
            "lastPrice": data.get("lastPrice"),
            "lastQty": data.get("lastQty"),
            "bidPrice": data.get("bidPrice"),
            "bidQty": data.get("bidQty"),
            "askPrice": data.get("askPrice"),
            "askQty": data.get("askQty"),
            "openPrice": data.get("openPrice"),
            "highPrice": data.get("highPrice"),
            "lowPrice": data.get("lowPrice"),
            "volume": data.get("volume"),
            "quoteVolume": data.get("quoteVolume"),
            "openTime": datetime.utcfromtimestamp(int(data.get("openTime", 0)) / 1000).strftime('%Y-%m-%d %H:%M:%S'),
            "closeTime": datetime.utcfromtimestamp(int(data.get("closeTime", 0)) / 1000).strftime('%Y-%m-%d %H:%M:%S'),
            "firstId": data.get("firstId"),
            "lastId": data.get("lastId"),
            "count": data.get("count")
        }
    except (KeyError, ValueError) as e:
        return {"error": str(e)}

@app.route('/prices')
def get_prices():
    coin_data = [get_coin_data(coin) for coin in coins]
    return jsonify(coin_data)

@app.route('/save_prices')
def save_prices():
    coin_data = [get_coin_data(coin) for coin in coins]
    df = pd.DataFrame(coin_data)
    df.to_csv("coin_data.csv", index=False)
    return "Data saved to coin_data.csv"

if __name__ == '__main__':
    app.run(debug=True)