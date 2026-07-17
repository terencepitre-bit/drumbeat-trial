
import os, datetime, json
from pathlib import Path
import feedparser, requests
from jinja2 import Template
from dateutil import parser as dateparser

def get_mortgage():
    try:
        key = os.getenv("FRED_API_KEY")
        if not key: return "6.89%"
        r = requests.get(f"https://api.stlouisfed.org/fred/series/observations?series_id=MORTGAGE30US&api_key={key}&file_type=json&sort_order=desc&limit=1", timeout=10)
        return f"{float(r.json()['observations'][0]['value']):.2f}%" if r.ok else "6.89%"
    except: return "6.89%"

def main():
    today = datetime.date.today().isoformat()
    out_dir = Path(f"issues/{today}")
    out_dir.mkdir(parents=True, exist_ok=True)
    # minimal template
    template = Path("issue_template.html").read_text() if Path("issue_template.html").exists() else "<html><body><h1>{{date}}</h1><p>Mortgage {{mortgage_rate}}</p><p>Only corrections@thedailydrumbeat.com and editor@thedailydrumbeat.com</p></body></html>"
    html = Template(template).render(date=today, mortgage_rate=get_mortgage(), drum_roll=[], money_box=[], hbcu=[], green_book=[], crypto=[])
    (out_dir / "index.html").write_text(html)
    # also update root index if needed
    Path("index.html").write_text(html) if not Path("index.html").exists() or len(Path("index.html").read_text())<200 else None

if __name__ == "__main__":
    main()
