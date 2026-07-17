
import os, shutil
from datetime import datetime

now = datetime.now()
date_str = now.strftime("%Y-%m-%d")
day_upper = now.strftime("%A %B %d %Y").upper()
day_title = now.strftime("%A %B %d %Y")

print(f"Building {date_str} - minimal safe mode")

# Load template
with open("issue_template.html", "r", encoding="utf-8") as f:
    html = f.read()

# Update dates only - no API calls, no RSS, cannot fail
html = html.replace("July 18 2026", day_title)
html = html.replace("JULY 18 2026", day_upper)
html = html.replace("2026-07-18", date_str)
html = html.replace("July 17 2026", day_title)
html = html.replace("JULY 17 2026", day_upper)
html = html.replace("2026-07-17", date_str)

with open("index.html", "w", encoding="utf-8") as out:
    out.write(html)

os.makedirs(f"issues/{date_str}", exist_ok=True)
with open(f"issues/{date_str}/index.html", "w", encoding="utf-8") as out:
    out.write(html)

print(f"✅ Built {date_str} - Landing + Today's Edition preserved, no external APIs")
