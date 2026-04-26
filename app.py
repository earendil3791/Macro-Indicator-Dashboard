import streamlit as st
import pandas as pd
from data_fetcher import load_series

st.set_page_config(page_title="Macro Dashboard", layout="wide")
st.title("Macro Data for Stock Investors")
tab_main, tab_basic, tab_etc = st.tabs(["IndexMain", "IndexBasic", "IndexETC"])

# ============================================================
# IndexMain
# ============================================================
with tab_main:
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("01. LEI - US Leading Indicators")
        st.line_chart(load_series("lei"))

        st.subheader("02. ISM Manufacturing PMI")
        st.warning("ISM headline PMI is not on FRED. Use S&P Global PMI (FRED: OUTMS) or paste ISM CSV manually.")
        st.line_chart(load_series("pmi"))

        st.subheader("03. Fear & Greed Index")
        st.warning("CNN Fear & Greed has no public API. Update manually or embed CNN's iframe.")

        st.subheader("05. JOLTs - Job Openings")
        st.line_chart(load_series("jolts"))

        st.subheader("06. FINRA Margin Debt")
        st.warning("Download monthly CSV from finra.org and load via pd.read_csv().")

    with c2:
        st.subheader("04. Buffett Indicator (Components)")
        st.info("Ratio = Wilshire 5000 / GDP. Charting both components separately.")
        w5k = load_series("wilshire")
        gdp = load_series("gdp")
        st.line_chart(pd.concat([w5k, gdp], axis=1))

        st.subheader("07. Michigan Consumer Sentiment")
        st.line_chart(load_series("michigan"))

        st.subheader("08. Shiller CAPE")
        st.warning("Source: multpl.com or Yale Shiller data. Not on FRED.")

# ============================================================
# IndexBasic
# ============================================================
with tab_basic:
    c1, c2, c3 = st.columns(3)

    with c1:
        st.subheader("US Dollar Index (DXY)")
        st.line_chart(load_series("dxy"))

        st.subheader("Treasury Yields")
        y1 = load_series("yield_1y")
        y2 = load_series("yield_2y")
        y10 = load_series("yield_10y")
        y30 = load_series("yield_30y")
        yields = pd.concat([y1, y2, y10, y30], axis=1).dropna()
        st.line_chart(yields)

        st.subheader("Yield Curve (10Y - 2Y)")
        spread = y10 - y2
        spread.name = "10Y-2Y Spread"
        st.line_chart(spread)

    with c2:
        st.subheader("M2 Money Supply")
        st.line_chart(load_series("m2"))

        st.subheader("Fed Balance Sheet")
        st.line_chart(load_series("fed_bs"))

        st.subheader("TGA Balance")
        st.line_chart(load_series("tga"))

        st.subheader("RRP")
        st.line_chart(load_series("rrp"))

    with c3:
        st.subheader("Russell 2000")
        st.line_chart(load_series("russell"))

        st.subheader("Gold")
        st.line_chart(load_series("gold"))

        st.subheader("WTI Crude")
        st.line_chart(load_series("wti"))

        st.subheader("Brent Crude")
        st.line_chart(load_series("brent"))

        st.subheader("30Y Mortgage Rate")
        st.line_chart(load_series("mortgage30"))

# ============================================================
# IndexETC
# ============================================================
with tab_etc:
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("CPI YoY")
        st.line_chart(load_series("cpi_yoy"))

        st.subheader("Core CPI YoY")
        st.line_chart(load_series("core_cpi_yoy"))

        st.subheader("PPI YoY")
        st.line_chart(load_series("ppi_yoy"))

        st.subheader("Core PCE YoY")
        st.line_chart(load_series("core_pce_yoy"))

        st.subheader("Michigan Inflation Expectations")
        st.line_chart(load_series("mich_infl_exp"))

    with c2:
        st.subheader("Retail Sales MoM")
        retail = load_series("retail")
        mom = retail.pct_change() * 100
        mom.name = "Retail Sales MoM %"
        st.line_chart(mom)

        st.subheader("Consumer Confidence (Conference Board)")
        st.warning("FRED code is typically CONF. Verify at fred.stlouisfed.org.")
        st.line_chart(load_series("conf"))

        st.subheader("High Yield OAS")
        st.line_chart(load_series("hy_oas"))

        st.subheader("Corporate OAS")
        st.line_chart(load_series("corp_oas"))

        st.subheader("Global Commodity Index")
        st.line_chart(load_series("commodities"))

        st.subheader("GDPNow (Atlanta Fed)")
        st.warning("Source: atlantafed.org/cgdpnow. No FRED series. Paste manually.")

st.caption("Sources: FRED / St. Louis Fed, Yahoo Finance. Data refreshed daily via GitHub Actions.")