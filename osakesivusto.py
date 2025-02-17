import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import ta

# 🌟 Uusi tumma teema ja parempi ulkoasu
st.set_page_config(page_title="Osakeanalyysi", layout="wide")

st.markdown(
    """
    <style>
        body {
            background-color: #121212;
            color: white;
            font-family: Arial, sans-serif;
        }
        .stApp {
            background-color: #121212;
        }
        .stTitle, .stHeader, .stTextInput, .stButton {
            color: white;
        }
        .card {
            background-color: #1E1E1E;
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0px;
        }
        .stButton>button {
            background-color: #00b4d8;
            color: white;
            border-radius: 5px;
            font-size: 16px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# 🌟 Sivun otsikko
st.title("📈 Osakeanalyysi - Täydellinen versio")

# 🌟 Käyttäjä syöttää osakkeiden tunnukset
symbol1 = st.text_input("🔍 Syötä ensimmäinen osake (esim. AAPL, TSLA)", "AAPL")
symbol2 = st.text_input("🔍 Syötä toinen osake (esim. MSFT, NVDA)", "MSFT")

# 🔍 Kun käyttäjä painaa nappia, haetaan tiedot
if st.button("Hae osaketiedot"):
    try:
        # 📊 Haetaan osaketiedot Yahoo Financesta
        stock1 = yf.Ticker(symbol1)
        stock2 = yf.Ticker(symbol2)

        data1 = stock1.history(period="6mo")
        data2 = stock2.history(period="6mo")

        # 📌 Lasketaan tekniset indikaattorit (RSI, MACD)
        data1['RSI'] = ta.momentum.RSIIndicator(data1['Close'], window=14).rsi()
        data1['MACD'] = ta.trend.MACD(data1['Close']).macd()

        data2['RSI'] = ta.momentum.RSIIndicator(data2['Close'], window=14).rsi()
        data2['MACD'] = ta.trend.MACD(data2['Close']).macd()

        # 📌 Näytetään osakkeiden perustiedot kortissa
        for stock, symbol in zip([stock1, stock2], [symbol1, symbol2]):
            info = stock.info
            st.markdown(f"""
                <div class="card">
                    <h2>{symbol} - Osakkeen tiedot</h2>
                    <p><b>📌 Osakkeen hinta:</b> {info.get('currentPrice', 'Ei saatavilla')} USD</p>
                    <p><b>🏦 Markkina-arvo:</b> {info.get('marketCap', 'Ei saatavilla')} USD</p>
                    <p><b>📊 P/E-luku:</b> {info.get('trailingPE', 'Ei saatavilla')}</p>
                    <p><b>💰 Osinkotuotto:</b> {info.get('dividendYield', 'Ei saatavilla')}</p>
                </div>
            """, unsafe_allow_html=True)

        # 📈 Piirretään hintakaavio
        st.subheader("📈 Osakkeiden hintakehitys (6kk)")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(data1.index, data1["Close"], label=f"{symbol1} Sulkemishinta", color="cyan")
        ax.plot(data2.index, data2["Close"], label=f"{symbol2} Sulkemishinta", color="magenta")
        ax.set_facecolor("#1E1E1E")
        ax.set_xlabel("Päivämäärä", color="white")
        ax.set_ylabel("Hinta ($)", color="white")
        ax.legend()
        st.pyplot(fig)

        # 📊 RSI ja MACD-kaaviot
        st.subheader("📊 RSI-indikaattori")
        fig, ax = plt.subplots(figsize=(10, 3))
        ax.plot(data1.index, data1["RSI"], label=f"{symbol1} RSI", color="cyan")
        ax.plot(data2.index, data2["RSI"], label=f"{symbol2} RSI", color="magenta")
        ax.axhline(70, linestyle="--", color="red", label="Yliostettu")
        ax.axhline(30, linestyle="--", color="green", label="Ylimyyty")
        ax.set_facecolor("#1E1E1E")
        ax.legend()
        st.pyplot(fig)

        st.subheader("📊 MACD-indikaattori")
        fig, ax = plt.subplots(figsize=(10, 3))
        ax.plot(data1.index, data1["MACD"], label=f"{symbol1} MACD", color="cyan")
        ax.plot(data2.index, data2["MACD"], label=f"{symbol2} MACD", color="magenta")
        ax.axhline(0, linestyle="--", color="gray")
        ax.set_facecolor("#1E1E1E")
        ax.legend()
        st.pyplot(fig)

        # 📌 Osto- ja myyntisuositukset RSI:n perusteella
        rsi1 = data1['RSI'].iloc[-1]
        rsi2 = data2['RSI'].iloc[-1]

        st.subheader("📊 Osto- ja myyntisuositukset")
        if rsi1 < 30:
            st.success(f"📈 {symbol1}: RSI {rsi1:.2f} → **Ostosignaali** (ylimyyty)")
        elif rsi1 > 70:
            st.warning(f"📉 {symbol1}: RSI {rsi1:.2f} → **Myyntisignaali** (yliostettu)")
        else:
            st.info(f"ℹ️ {symbol1}: RSI {rsi1:.2f} → Neutraali")

        if rsi2 < 30:
            st.success(f"📈 {symbol2}: RSI {rsi2:.2f} → **Ostosignaali** (ylimyyty)")
        elif rsi2 > 70:
            st.warning(f"📉 {symbol2}: RSI {rsi2:.2f} → **Myyntisignaali** (yliostettu)")
        else:
            st.info(f"ℹ️ {symbol2}: RSI {rsi2:.2f} → Neutraali")

    except Exception as e:
        st.error(f"⚠️ Virhe osaketietojen haussa: {e}")
