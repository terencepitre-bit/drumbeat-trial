
"""
The Daily Drumbeat - Live Trial - Dynamic RSS version
Generates fresh issues with live RSS each run
"""
import os
import feedparser
import requests
from datetime import datetime
from jinja2 import Template

def fetch_rss(url, limit=2):
    try:
        feed = feedparser.parse(url)
        return feed.entries[:limit]
    except Exception as e:
        print(f"RSS fail {url}: {e}")
        return []

def get_mortgage_rate():
    fred_key = os.getenv("FRED_API_KEY")
    if fred_key:
        try:
            url = f"https://api.stlouisfed.org/fred/series/observations?series_id=MORTGAGE30US&api_key={fred_key}&file_type=json&sort_order=desc&limit=1"
            r = requests.get(url, timeout=10).json()
            return float(r['observations'][0]['value'])
        except Exception as e:
            print(f"FRED fail: {e}")
    return 6.89

def get_crypto():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
        r = requests.get(url, timeout=10).json()
        return r['bitcoin']['usd'], r['ethereum']['usd']
    except:
        return 64034, 1883

def get_markets():
    return {
        "sp500": "7,572.40",
        "dow": "52,658.64",
        "uone": "$5.05 +1.0%",
        "rlj": "$11.71 +0.9%",
        "carv": "$1.40 +0.0%"
    }

def build_issue():
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    day_name = now.strftime("%A, %B %d, %Y")
    
    RSS_FEEDS = {
        "policy": ["https://thegrio.com/feed/", "https://www.blackenterprise.com/feed/", "https://www.theroot.com/rss"],
        "business": ["https://www.blackenterprise.com/feed/", "https://blavity.com/feed", "https://www.blackbusiness.com/feed/"],
        "hbcu": ["https://hbcugameday.com/feed/", "https://hbcubuzz.com/feed/"]
    }
    
    policy_entries = []
    for url in RSS_FEEDS["policy"]:
        policy_entries += fetch_rss(url, 2)
    
    business_entries = []
    for url in RSS_FEEDS["business"]:
        business_entries += fetch_rss(url, 2)

    hbcu_entries = []
    for url in RSS_FEEDS["hbcu"]:
        hbcu_entries += fetch_rss(url, 2)

    mortgage = get_mortgage_rate()
    btc, eth = get_crypto()
    markets = get_markets()

    template_path = "issue_template.html"
    if not os.path.exists(template_path):
        print(f"Missing {template_path}")
        return
        
    template = Template(open(template_path, encoding="utf-8").read())
    html = template.render(
        date_str=date_str,
        day_name=day_name,
        mortgage=mortgage,
        btc=btc,
        eth=eth,
        markets=markets,
        policy=policy_entries[:4],
        business=business_entries[:4],
        hbcu=hbcu_entries[:2],
        vol="1",
        no=str(now.timetuple().tm_yday)
    )
    
    out_path = f"issues/{date_str}/index.html"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"Generated {out_path} - {len(policy_entries)} policy, {len(business_entries)} business, {len(hbcu_entries)} hbcu - Mortgage {mortgage}% BTC ${btc}")

if __name__ == "__main__":
    build_issue()
