st.header("🔥 Live NSE Stock Screener")

nse_stocks = [
    "RELIANCE.NS","TCS.NS","INFY.NS","HDFCBANK.NS",
    "ICICIBANK.NS","SBIN.NS","ITC.NS","LT.NS"
]

screened = []

for stock in nse_stocks:

    try:
        data = yf.download(stock, period="1y", progress=False)

        data["MA50"] = data["Close"].rolling(50).mean()
        data["MA200"] = data["Close"].rolling(200).mean()

        rsi = RSIIndicator(data["Close"]).rsi()

        latest_price = data["Close"].iloc[-1]
        latest_rsi = rsi.iloc[-1]

        avg_vol = data["Volume"].tail(20).mean()
        latest_vol = data["Volume"].iloc[-1]

        if (
            latest_price > data["MA200"].iloc[-1]
            and latest_rsi < 70
            and latest_vol > avg_vol * 1.5
        ):
            screened.append([
                stock,
                round(latest_price,2),
                round(latest_rsi,2)
            ])

    except:
        pass

st.dataframe(
    pd.DataFrame(
        screened,
        columns=["Stock","Price","RSI"]
    )
)