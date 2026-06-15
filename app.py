import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Teen Stock Screener",
    page_icon="📈",
    layout="wide",
)

# ── CUSTOM CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif; }

    .hero {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%);
        border-radius: 16px;
        padding: 40px 48px;
        margin-bottom: 32px;
        color: white;
    }
    .hero h1 { font-size: 2.6rem; font-weight: 700; margin: 0 0 8px 0; letter-spacing: -0.5px; }
    .hero p  { font-size: 1.05rem; color: #94a3b8; margin: 0; }
    .hero span { color: #38bdf8; }

    .explain-box {
        background: #eff6ff;
        border-left: 4px solid #3b82f6;
        border-radius: 0 8px 8px 0;
        padding: 16px 20px;
        margin: 8px 0 16px 0;
    }
    .explain-box p { font-size: 0.88rem; color: #1e3a5f; margin: 0; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

# ── TICKERS ───────────────────────────────────────────────────────────────────
TICKERS = [
    "AAPL","MSFT","GOOGL","AMZN","META","TSLA","NVDA","AMD",
    "NFLX","DIS","SPOT","SNAP","RBLX","NKE","SBUX","MCD",
    "KO","PEP","JNJ","JPM","BAC","V","MA","PYPL",
    "COST","WMT","TGT","HD","LOW","F","GM","UBER",
]

EXPLANATIONS = {
    "Price ($)": (
        "**What it means:** The cost to buy one share right now.\n\n"
        "Don't judge a stock by price alone — a $5 stock isn't automatically cheaper "
        "than a $500 one. What matters is the value you get for that price."
    ),
    "P/E Ratio": (
        "**What it means:** How much you pay per $1 of profit the company makes.\n\n"
        "- Under 15 → Potentially cheap\n"
        "- 15–25 → Normal / fairly priced\n"
        "- Over 40 → Expensive (market expects big growth)\n\n"
        "Example: P/E of 20 = paying $20 for every $1 the company earns."
    ),
    "Mkt Cap ($B)": (
        "**What it means:** Total value of all the company's shares combined.\n\n"
        "- Over $10B → Large-cap (stable giants like Apple, Google)\n"
        "- $2B–$10B → Mid-cap (growing companies)\n"
        "- Under $2B → Small-cap (riskier, but more potential upside)"
    ),
    "Div Yield (%)": (
        "**What it means:** Cash the company pays you per year just for holding the stock.\n\n"
        "Example: 3% yield on $1,000 = $30/year automatically deposited.\n\n"
        "Growth stocks like Tesla pay $0 — they reinvest all profits instead."
    ),
    "Beta": (
        "**What it means:** How much the stock swings vs. the overall market.\n\n"
        "- Over 1.0 → More volatile than the market\n"
        "- Exactly 1.0 → Moves with the market\n"
        "- Under 1.0 → More stable than the market\n\n"
        "Example: Tesla beta ~2 means if the market drops 10%, Tesla might drop 20%."
    ),
    "Volume (M)": (
        "**What it means:** How many millions of shares were traded today.\n\n"
        "High volume = easy to buy/sell quickly.\n"
        "Low volume = harder to exit a position fast.\n"
        "Sudden spikes often signal big news."
    ),
    "52W High ($)": (
        "**What it means:** The highest price the stock hit in the last 52 weeks.\n\n"
        "Near its 52W high = strong recent momentum.\n"
        "Far below it = big drop happened — always research why."
    ),
    "52W Low ($)": (
        "**What it means:** The lowest price over the last year.\n\n"
        "Near the low could mean a bargain — or a real problem with the company.\n"
        "Always research before buying a stock near its 52W low."
    ),
}

# ── DATA FETCH ────────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def fetch_data(tickers):
    rows = []
    for ticker in tickers:
        try:
            info     = yf.Ticker(ticker).info
            price    = info.get("currentPrice") or info.get("regularMarketPrice")
            pe       = info.get("trailingPE")
            mktcap   = info.get("marketCap")
            div_yld  = info.get("dividendYield")
            sector   = info.get("sector", "N/A")
            volume   = info.get("regularMarketVolume")
            high_52w = info.get("fiftyTwoWeekHigh")
            low_52w  = info.get("fiftyTwoWeekLow")
            beta     = info.get("beta")
            name     = info.get("shortName", ticker)
            rows.append({
                "Ticker":        ticker,
                "Company":       name,
                "Price ($)":     round(price,   2) if price   else None,
                "P/E Ratio":     round(pe,      1) if pe      else None,
                "Mkt Cap ($B)":  round(mktcap / 1e9, 1) if mktcap else None,
                "Div Yield (%)": round(div_yld * 100, 2) if div_yld else 0.0,
                "Sector":        sector,
                "Volume (M)":    round(volume / 1e6, 2) if volume else None,
                "52W High ($)":  round(high_52w, 2) if high_52w else None,
                "52W Low ($)":   round(low_52w,  2) if low_52w  else None,
                "Beta":          round(beta,     2) if beta     else None,
            })
        except Exception:
            pass
    return pd.DataFrame(rows)

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>📈 Teen Stock Screener</h1>
    <p>Filter real stocks by real metrics — with plain-English explanations of what everything means.<br>
    Built for <span>teenagers learning to invest</span>.</p>
</div>
""", unsafe_allow_html=True)

# ── LOAD DATA ─────────────────────────────────────────────────────────────────
with st.spinner("Fetching live market data... (~15 seconds on first load)"):
    df = fetch_data(tuple(TICKERS))

if df.empty:
    st.error("Could not load stock data. Check your internet connection and try again.")
    st.stop()

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
st.sidebar.markdown("## 🔍 Filters")
st.sidebar.caption("Adjust sliders to narrow results.")

sectors      = ["All"] + sorted(df["Sector"].dropna().unique().tolist())
sel_sector   = st.sidebar.selectbox("Sector", sectors)

price_max    = st.sidebar.slider("Max Price ($)",          0,   2000, 2000, step=10)
pe_max       = st.sidebar.slider("Max P/E Ratio",          0,    100,  100, step=1)
mktcap_min   = st.sidebar.slider("Min Market Cap ($B)",    0,    500,    0, step=5)
div_min      = st.sidebar.slider("Min Dividend Yield (%)", 0.0, 10.0,  0.0, step=0.1)
beta_max     = st.sidebar.slider("Max Beta",               0.0,  5.0,  5.0, step=0.1)
vol_min      = st.sidebar.slider("Min Volume (M shares)",  0.0, 100.0, 0.0, step=1.0)

st.sidebar.markdown("---")
st.sidebar.markdown("### 💡 What does this mean?")
metric_choice = st.sidebar.selectbox("Pick a metric to explain", list(EXPLANATIONS.keys()))
st.sidebar.markdown(
    f'<div class="explain-box"><p>{EXPLANATIONS[metric_choice]}</p></div>',
    unsafe_allow_html=True
)

# ── APPLY FILTERS ─────────────────────────────────────────────────────────────
f = df.copy()
if sel_sector != "All":
    f = f[f["Sector"] == sel_sector]
f = f[f["Price ($)"].fillna(99999)    <= price_max]
f = f[f["P/E Ratio"].fillna(99999)    <= pe_max]
f = f[f["Mkt Cap ($B)"].fillna(0)     >= mktcap_min]
f = f[f["Div Yield (%)"].fillna(0)    >= div_min]
f = f[f["Beta"].fillna(99999)         <= beta_max]
f = f[f["Volume (M)"].fillna(0)       >= vol_min]

# ── SUMMARY CARDS ─────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("Stocks shown",  len(f), f"of {len(df)} total")
c2.metric("Avg P/E",       f"{f['P/E Ratio'].mean():.1f}"    if not f.empty else "—")
c3.metric("Avg Div Yield", f"{f['Div Yield (%)'].mean():.2f}%" if not f.empty else "—")
c4.metric("Avg Beta",      f"{f['Beta'].mean():.2f}"         if not f.empty else "—")

st.markdown("---")

# ── TABLE ─────────────────────────────────────────────────────────────────────
if f.empty:
    st.warning("No stocks match your filters — try loosening one of the sliders.")
else:
    st.markdown(f"### Results — {len(f)} stocks")
    st.dataframe(
        f.reset_index(drop=True),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Ticker":        st.column_config.TextColumn("Ticker",       width="small"),
            "Company":       st.column_config.TextColumn("Company"),
            "Price ($)":     st.column_config.NumberColumn("Price",      format="$%.2f"),
            "P/E Ratio":     st.column_config.NumberColumn("P/E",        format="%.1f"),
            "Mkt Cap ($B)":  st.column_config.NumberColumn("Mkt Cap",    format="$%.1fB"),
            "Div Yield (%)": st.column_config.NumberColumn("Div Yield",  format="%.2f%%"),
            "Sector":        st.column_config.TextColumn("Sector"),
            "Volume (M)":    st.column_config.NumberColumn("Volume",     format="%.1fM"),
            "52W High ($)":  st.column_config.NumberColumn("52W High",   format="$%.2f"),
            "52W Low ($)":   st.column_config.NumberColumn("52W Low",    format="$%.2f"),
            "Beta":          st.column_config.NumberColumn("Beta",       format="%.2f"),
        }
    )

    # ── CHART ─────────────────────────────────────────────────────────────────
    chart_df = f.dropna(subset=["P/E Ratio", "Mkt Cap ($B)", "Volume (M)"])
    if not chart_df.empty:
        st.markdown("### 📊 P/E Ratio vs. Market Cap")
        st.caption("Bubble size = daily trading volume. Hover a stock for full details.")
        fig = px.scatter(
            chart_df,
            x="Mkt Cap ($B)",
            y="P/E Ratio",
            text="Ticker",
            color="Sector",
            size="Volume (M)",
            size_max=50,
            hover_data=["Company", "Price ($)", "Div Yield (%)", "Beta"],
            template="plotly_white",
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        fig.update_traces(textposition="top center", marker=dict(opacity=0.8, line=dict(width=1, color="white")))
        fig.update_layout(
            font_family="Inter",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=0, r=0, t=48, b=0),
        )
        st.plotly_chart(fig, use_container_width=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='color:#94a3b8; font-size:0.8rem; text-align:center;'>"
    "Data via Yahoo Finance · Updates every hour · For educational use only — not financial advice."
    "</p>",
    unsafe_allow_html=True,
)
