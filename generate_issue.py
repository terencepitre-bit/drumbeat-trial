import os
import feedparser
import requests
from datetime import datetime
from jinja2 import Template

def fetch_rss(url, limit=3):
    try:
        return feedparser.parse(url).entries[:limit]
    except:
        return []

def get_mortgage_rate():
    fred_key = os.getenv("FRED_API_KEY")
    if fred_key:
        try:
            url = f"https://api.stlouisfed.org/fred/series/observations?series_id=MORTGAGE30US&api_key={fred_key}&file_type=json&sort_order=desc&limit=1"
            r = requests.get(url, timeout=10).json()
            return float(r['observations'][0]['value'])
        except:
            pass
    return 6.89

def get_crypto():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
        r = requests.get(url, timeout=10).json()
        return r['bitcoin']['usd'], r['ethereum']['usd']
    except:
        return 64034, 1883

def build_issue():
    date_str = datetime.now().strftime("%Y-%m-%d")
    day_name = datetime.now().strftime("%A, %B %d, %Y")
    policy = fetch_rss("https://thegrio.com/feed/", 2)
    business = fetch_rss("https://www.blackenterprise.com/feed/", 2)
    hbcu = fetch_rss("https://hbcugameday.com/feed/", 2)
    mortgage = get_mortgage_rate()
    btc, eth = get_crypto()
    markets = {"sp500": "7,572.40", "dow": "52,658.64", "uone": "$5.05 +1.0%"}
    template = Template(open("issue_template.html", encoding="utf-8").read())
    html = template.render(date_str=date_str, day_name=day_name, mortgage=mortgage, btc=btc, eth=eth, markets=markets, policy=policy, business=business, hbcu=hbcu, vol="1", no="5")
    out_path = f"issues/{date_str}/index.html"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated {out_path}")

if __name__ == "__main__":
    build_issue()
