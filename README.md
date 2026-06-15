# 📈 Teen Stock Screener

A free, interactive stock screener built for teenagers learning to invest — with plain-English explanations of every metric.

[![Open App](https://img.shields.io/badge/Open%20App-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://your-app-name.streamlit.app)

---

## What it does

- Pulls **live data** for 32 stocks teenagers actually know (Apple, Tesla, Nike, Spotify, Roblox, and more)
- Filter by **price, P/E ratio, market cap, dividend yield, sector, beta, and volume**
- Every metric comes with a **plain-English explanation** — no finance background needed
- Interactive **scatter chart** showing P/E vs. Market Cap by sector
- Data refreshes automatically every hour via Yahoo Finance

## Why I built this

Financial literacy is a gap that hurts young people most. This tool is part of a broader mission — [Cents & Sense](https://github.com), a free virtual financial literacy program I co-founded for middle and high schoolers. The screener gives teens a hands-on way to explore the market using companies they already know.

## Tech stack

- **Python** + **Streamlit** — web app framework
- **yfinance** — free Yahoo Finance API wrapper
- **Plotly** — interactive charting
- **Pandas** — data filtering and manipulation

## Run it locally

```bash
git clone https://github.com/YOUR_USERNAME/teen-stock-screener
cd teen-stock-screener
pip install -r requirements.txt
streamlit run app.py
```

## Deploy your own copy

1. Fork this repo
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub and select this repo
4. Set main file to `app.py` → Deploy

---

*Data provided by Yahoo Finance. For educational use only — not financial advice.*
