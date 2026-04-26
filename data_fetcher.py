import os
from datetime import datetime, timedelta
import pandas as pd
from fredapi import Fred
import yfinance as yf

FRED_API_KEY = os.getenv("FRED_API_KEY", "c5dbf581c631ec858f615fda7fdabde6")
fred = Fred(api_key=FRED_API_KEY)
START = (datetime.now() - timedelta(days=5*365)).strftime("%Y-%m-%d")

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def save_series(series: pd.Series, filename: str):
    path = os.path.join(DATA_DIR, f"{filename}.json")
    series.to_json(path, date_format="iso")

def load_series(filename: str) -> pd.Series:
    path = os.path.join(DATA_DIR, f"{filename}.json")
    if not os.path.exists(path):
        return pd.Series(name=filename)
    return pd.read_json(path, typ="series")

def fetch_fred(series_id: str, name: str = None) -> pd.Series:
    try:
        s = fred.get_series(series_id, observation_start=START)
        s.name = name or series_id
        return s
    except Exception:
        return pd.Series(name=name or series_id)

def fetch_yf(ticker: str, name: str = None, period: str = "5y") -> pd.Series:
    try:
        hist = yf.Ticker(ticker).history(period=period)
        s = hist["Close"].copy()
        s.name = name or ticker
        return s
    except Exception:
        return pd.Series(name=name or ticker)

def fetch_yoy(series_id: str, name: str) -> pd.Series:
    s = fetch_fred(series_id, name)
    if s.empty:
        return s
    yoy = s.pct_change(periods=12) * 100
    yoy.name = f"{name} YoY %"
    return yoy

# ============================================================
# CACHE ALL INDICATORS (run by GitHub Actions daily at 9 AM)
# ============================================================
if __name__ == "__main__":
    print(f"Starting data refresh at {datetime.now()}")

    # IndexMain
    save_series(fetch_fred("USSLIND", "LEI"), "lei")
    save_series(fetch_fred("OUTMS", "S&P Global Manufacturing PMI"), "pmi")
    save_series(fetch_fred("JTSJOL", "JOLTs Job Openings"), "jolts")
    save_series(fetch_fred("WILL5000INDFC", "Wilshire 5000"), "wilshire")
    save_series(fetch_fred("GDP", "Nominal GDP"), "gdp")
    save_series(fetch_fred("UMCSENT", "Michigan Sentiment"), "michigan")

    # IndexBasic
    save_series(fetch_fred("DTWEXBGS", "DXY"), "dxy")
    save_series(fetch_fred("DGS1", "1Y"), "yield_1y")
    save_series(fetch_fred("DGS2", "2Y"), "yield_2y")
    save_series(fetch_fred("DGS10", "10Y"), "yield_10y")
    save_series(fetch_fred("DGS30", "30Y"), "yield_30y")
    save_series(fetch_fred("M2SL", "M2"), "m2")
    save_series(fetch_fred("WALCL", "Fed Total Assets"), "fed_bs")
    save_series(fetch_fred("WDTGAL", "Treasury General Account"), "tga")
    save_series(fetch_fred("RRPONTSYD", "Overnight RRP"), "rrp")
    save_series(fetch_fred("MORTGAGE30US", "30Y Mortgage"), "mortgage30")
    save_series(fetch_yf("^RUT", "Russell 2000"), "russell")
    save_series(fetch_yf("GC=F", "Gold Futures"), "gold")
    save_series(fetch_yf("CL=F", "WTI Crude"), "wti")
    save_series(fetch_yf("BZ=F", "Brent Crude"), "brent")

    # IndexETC
    save_series(fetch_yoy("CPIAUCSL", "CPI"), "cpi_yoy")
    save_series(fetch_yoy("CPILFESL", "Core CPI"), "core_cpi_yoy")
    save_series(fetch_yoy("PPIACO", "PPI"), "ppi_yoy")
    save_series(fetch_yoy("PCEPILFE", "Core PCE"), "core_pce_yoy")
    save_series(fetch_fred("MICH", "1Y Inflation Expectations"), "mich_infl_exp")
    save_series(fetch_fred("RSAFS", "Retail Sales"), "retail")
    save_series(fetch_fred("CONF", "Consumer Confidence"), "conf")
    save_series(fetch_fred("BAMLH0A1HYBB", "HY OAS"), "hy_oas")
    save_series(fetch_fred("BAMLC0A3CA", "Corp OAS"), "corp_oas")
    save_series(fetch_fred("PALLFNFINDEXM", "All Commodities"), "commodities")

    print(f"Data refresh complete at {datetime.now()}")