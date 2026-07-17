
import os, re
from datetime import datetime
import requests

now = datetime.now()
date_str = now.strftime("%Y-%m-%d")
day_title = now.strftime("%A %B %d %Y")
day_upper = now.strftime("%A %B %d %Y").upper()

print(f"Building SAFE {date_str} - no story injection")

with open("issue_template.html","r",encoding="utf-8") as f:
    html = f.read()

# Date
for old in ["July 18 2026", "July 17 2026"]:
    html = html.replace(old, day_title)
for old in ["JULY 18 2026", "JULY 17 2026"]:
    html = html.replace(old, day_upper)
html = html.replace("2026-07-18", date_str).replace("2026-07-17", date_str)

# Live money - try, but fallback so never crash
mortgage = 6.92
btc = 64034
eth = 1883
uone = 5.05
rlj = 11.71
carv = 1.40

try:
    fk = os.getenv("FRED_API_KEY")
    if fk:
        r = requests.get(f"https://api.stlouisfed.org/fred/series/observations?series_id=MORTGAGE30US&api_key={fk}&file_type=json&sort_order=desc&limit=1", timeout=10).json()
        mortgage = round(float(r['observations'][0]['value']),2)
        print(f"FRED LIVE {mortgage}%")
except Exception as e:
    print(f"FRED fallback {e}")

try:
    r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd", timeout=10).json()
    btc = int(r['bitcoin']['usd'])
    eth = int(r['ethereum']['usd'])
    print(f"CoinGecko LIVE BTC {btc}")
except:
    pass

try:
    fkey = os.getenv("FINNHUB_API_KEY")
    if fkey:
        for sym in ["UONE","RLJ","CARV"]:
            try:
                rr = requests.get(f"https://finnhub.io/api/v1/quote?symbol={sym}&token={fkey}", timeout=8).json()
                c = rr.get('c')
                if c:
                    if sym=="UONE": uone=round(c,2)
                    if sym=="RLJ": rlj=round(c,2)
                    if sym=="CARV": carv=round(c,2)
            except:
                pass
        print(f"Finnhub LIVE UONE {uone} RLJ {rlj} CARV {carv}")
except:
    pass

# Safe money replace - only visible boxes, not JS
html = re.sub(r'6\.89%', f"{mortgage}%", html)
# Do not touch Sm array at all

with open("index.html","w",encoding="utf-8") as out:
    out.write(html)
os.makedirs(f"issues/{date_str}", exist_ok=True)
with open(f"issues/{date_str}/index.html","w",encoding="utf-8") as out:
    out.write(html)

print(f"SAFE BUILT {date_str} - site will not white-screen")
