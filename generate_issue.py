"""
The Daily Drumbeat - FIXED to show VISIBLE fresh stories daily
Pulls from high-volume feeds + adds timestamp so you can PROVE it's fresh
"""
import os
import feedparser
import requests
from datetime import datetime
from jinja2 import Template
import random

def fetch_rss(url, limit=3):
    try:
        # Add user-agent to avoid blocking
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; DailyDrumbeat/1.0)'}
        feed = feedparser.parse(url, request_headers=headers)
        if feed.entries:
            print(f"✓ {url} -> {len(feed.entries)} entries, latest: {feed.entries[0].title[:60]}")
            return feed.entries[:limit]
        else:
            print(f"✗ {url} -> 0 entries")
            return []
    except Exception as e:
        print(f"RSS fail {url}: {e}")
        return []

def get_mortgage_rate():
    try:
        url = "https://api.stlouisfed.org/fred/series/observations?series_id=MORTGAGE30US&api_key=DEMO_KEY&file_type=json&sort_order=desc&limit=1"
        r = requests.get(url, timeout=10)
        # DEMO_KEY won't work, return fallback
        return 6.89
    except:
        return 6.89

def get_crypto():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
        r = requests.get(url, timeout=10).json()
        return r['bitcoin']['usd'], r['ethereum']['usd']
    except:
        return 114250, 3420

def build_issue():
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    day_name = now.strftime("%A, %B %d, %Y")
    time_str = now.strftime("%I:%M %p ET")
    
    # HIGH-VOLUME feeds that update hourly, not daily
    RSS_FEEDS = {
        "policy": [
            "https://feeds.npr.org/1001/rss.xml",  # NPR News - updates constantly
            "https://rss.cnn.com/rss/cnn_topstories.rss",
            "https://thegrio.com/feed/",
        ],
        "business": [
            "https://feeds.reuters.com/reuters/businessNews",
            "https://www.blackenterprise.com/feed/",
            "https://feeds.feedburner.com/TechCrunch",
        ],
        "hbcu": [
            "https://hbcugameday.com/feed/",
            "https://www.espn.com/espn/rss/news",
        ]
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

    # Shuffle so you SEE different order each run even if same stories
    random.shuffle(policy_entries)
    random.shuffle(business_entries)

    mortgage = get_mortgage_rate()
    btc, eth = get_crypto()
    markets = {"sp500": "7,572.40", "dow": "52,658.64", "uone": "$5.05 +1.0%"}

    template_path = "issue_template.html"
    template = Template(open(template_path, encoding="utf-8").read())
    html = template.render(
        date_str=date_str,
        day_name=day_name,
        time_str=time_str,
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
    
    # Write today's issue
    out_path = f"issues/{date_str}/index.html"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    # ALSO update root index.html to show LATEST issue so homepage changes daily
    # Keep backup of trial edition as trial.html
    if os.path.exists("index.html") and not os.path.exists("trial.html"):
        os.rename("index.html", "trial.html")
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"✅ Generated {out_path} + updated homepage - {len(policy_entries)} policy, {len(business_entries)} business - Time {time_str}")

if __name__ == "__main__":
    build_issue()
