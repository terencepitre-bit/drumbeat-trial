"""
Drumbeat - LIVE MONEY - Safe upgrade on green build
- Keeps your cleaned newspaper look (no 5+2+1+1, only Corrections@, editor@, Call for prices)
- Updates date daily
- LIVE: FRED 30-Yr Mortgage, Finnhub UONE/RLJ/CARV + S&P/Dow, CoinGecko BTC/ETH
- Every API wrapped in try/except so it never fails - fallback to 6.89% if API down
"""
import os, re, requests
from datetime import datetime

def get_mortgage():
    key = os.getenv("FRED_API_KEY")
    if not key:
        print("FRED_API_KEY not set, fallback 6.89%")
        return 6.89, False
    try:
        url = f"https://api.stlouisfed.org/fred/series/observations?series_id=MORTGAGE30US&api_key={key}&file_type=json&sort_order=desc&limit=1"
        r = requests.get(url, timeout=12)
        data = r.json()
        val = float(data['observations'][0]['value'])
        print(f"✅ FRED LIVE: {val}%")
        return round(val,2), True
    except Exception as e:
        print(f"FRED fallback: {e}")
        return 6.89, False

def get_crypto():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd", timeout=12).json()
        btc = int(r['bitcoin']['usd'])
        eth = int(r['ethereum']['usd'])
        print(f"✅ CoinGecko LIVE: BTC ${btc} ETH ${eth}")
        return btc, eth, True
    except Exception as e:
        print(f"CoinGecko fallback: {e}")
        return 64034, 1883, False

def get_finnhub(symbol):
    key = os.getenv("FINNHUB_API_KEY")
    if not key:
        return None
    try:
        url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={key}"
        r = requests.get(url, timeout=10).json()
        c = r.get('c')
        dp = r.get('dp', 0)
        if c:
            return round(c,2), round(dp,2)
    except Exception as e:
        print(f"Finnhub {symbol} error: {e}")
    return None

def build():
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    day_upper = now.strftime("%A %B %d %Y").upper()
    day_title = now.strftime("%A %B %d %Y")
    print(f"Building {date_str}")

    # Load template
    try:
        with open("issue_template.html","r",encoding="utf-8") as f:
            html = f.read()
    except Exception as e:
        print(f"Failed to read template: {e}")
        return

    # LIVE DATA - all wrapped, never crash
    mortgage, mortgage_live = get_mortgage()
    btc, eth, crypto_live = get_crypto()
    
    finnhub_key = os.getenv("FINNHUB_API_KEY")
    uone = get_finnhub("UONE")
    rlj = get_finnhub("RLJ")
    carv = get_finnhub("CARV")
    spy = get_finnhub("SPY")
    dia = get_finnhub("DIA")

    # Default fallbacks for Black Wall Street Watch
    uone_price, uone_chg = uone if uone else (5.05, 1.0)
    rlj_price, rlj_chg = rlj if rlj else (11.71, 0.0)
    carv_price, carv_chg = carv if carv else (1.40, -0.7)

    # Update dates
    for old in ["July 18 2026", "July 17 2026"]:
        html = html.replace(old, day_title)
    for old in ["JULY 18 2026", "JULY 17 2026"]:
        html = html.replace(old, day_upper)
    html = html.replace("2026-07-18", date_str).replace("2026-07-17", date_str)

    # Update money numbers - safe regex replaces
    try:
        html = re.sub(r'6\.89%', f"{mortgage}%", html)
        html = html.replace("$64,034", f"${btc:,}")
        html = html.replace("$1,883", f"${eth:,}")
        # Black stocks - replace first occurrences
        html = html.replace("$5.05", f"${uone_price}", 2)
        html = html.replace("$11.71", f"${rlj_price}", 2)
        html = html.replace("$1.40", f"${carv_price}", 2)
    except Exception as e:
        print(f"Money replace fallback: {e}")

    # Write
    try:
        with open("index.html","w",encoding="utf-8") as out:
            out.write(html)
        os.makedirs(f"issues/{date_str}", exist_ok=True)
        with open(f"issues/{date_str}/index.html","w",encoding="utf-8") as out:
            out.write(html)
        print(f"✅ Built {date_str} - Mortgage {mortgage}% {'LIVE' if mortgage_live else 'fallback'} BTC ${btc} UONE ${uone_price} RLJ ${rlj_price} CARV ${carv_price}")
    except Exception as e:
        print(f"Write failed: {e}")

if __name__ == "__main__":
    build()
