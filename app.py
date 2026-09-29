import requests
import pandas as pd
import plotly.graph_objects as go

url = "https://api.coingecko.com/api/v3/coins/bitcoin/ohlc"

params = {
    "vs_currency": "usd",
    "days": "30"
}

response = requests.get(url, params=params)

data = response.json()

df = pd.DataFrame(
    data,
    columns=["timestamp", "Open", "High", "Low", "Close"]
)

df["Date"] = pd.to_datetime(df["timestamp"], unit="ms")

df = df[["Date", "Open", "High", "Low", "Close"]]

df["MA7"] = df["Close"].rolling(7).mean()

current_price = df["Close"].iloc[-1]
highest_price = df["High"].max()
lowest_price = df["Low"].min()

percentage_change = (
    (current_price - df["Open"].iloc[0])
    / df["Open"].iloc[0]
) * 100

print("\n--- Bitcoin Market Summary ---")
print(f"Current Price: ${current_price:,.2f}")
print(f"30-Day High: ${highest_price:,.2f}")
print(f"30-Day Low: ${lowest_price:,.2f}")
print(f"30-Day Change: {percentage_change:.2f}%")

fig = go.Figure()

fig.add_trace(
    go.Candlestick(
        x=df["Date"],
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name="Bitcoin"
    )
)

fig.add_trace(
    go.Scatter(
        x=df["Date"],
        y=df["MA7"],
        mode="lines",
        name="7-Period MA"
    )
)

fig.update_layout(
    title="Bitcoin 30-Day Candlestick Chart",
    xaxis_title="Date",
    yaxis_title="Price (USD)",
    xaxis_rangeslider_visible=False
)

fig.show()