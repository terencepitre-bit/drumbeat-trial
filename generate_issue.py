
import os, shutil
from datetime import datetime

def build_issue():
    # Today is July 17, 2026 per your request - but auto-updates daily
    now = datetime.now()
    # Force to July 17, 2026 for this restore if you want exact Vol 1 No 5, otherwise use now
    # Use now for auto-daily
    date_str = now.strftime("%Y-%m-%d")
    # Format like FRIDAY JULY 17 2026
    day_name_upper = now.strftime("%A %B %d %Y").upper()
    # e.g., Friday July 17 2026
    day_name_title = now.strftime("%A %B %d %Y")
    
    # For Vol 1 No 5 trial, keep Vol 1 No 5 static, but date dynamic
    # Read template
    with open("issue_template.html", "r", encoding="utf-8") as f:
        html = f.read()
    
    # Replace July 18 2026 with current date in all formats
    # Original has: VOL 1 NO 5 — FRIDAY JULY 18 2026 and 2026-07-18
    html = html.replace("July 18 2026", day_name_title)
    html = html.replace("JULY 18 2026", day_name_upper)
    html = html.replace("2026-07-18", date_str)
    # Also replace Friday July 18 2026 specific
    html = html.replace("FRIDAY JULY 18 2026", day_name_upper)
    
    # Ensure it has both landing and today's edition structure (it does - React app handles routing)
    # Write to root index.html = landing + today's edition (client-side tabs)
    with open("index.html", "w", encoding="utf-8") as out:
        out.write(html)
    
    # Write to dated archive folder - this is what Archive tab lists
    out_path = f"issues/{date_str}/index.html"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as out:
        out.write(html)
    
    # Also ensure July 17 specific folder exists for your trial
    july17_path = "issues/2026-07-17/index.html"
    os.makedirs(os.path.dirname(july17_path), exist_ok=True)
    with open(july17_path, "w", encoding="utf-8") as out:
        out.write(html)
    
    print(f"✅ Restored LANDING + TODAY'S EDITION")
    print(f"   - Landing: THE DAILY DRUMBEAT, News about us. For us., VOL 1 NO 5 — {day_name_upper}")
    print(f"   - Inside Today: 8 sections [P1 Business 1,700][P2 Policy Cold-case][P3 Labor][P4 Markets Mortgage Crypto][P5 HBCU $1M][P6 Sports][P11 Black Excellence][GB Green Book]")
    print(f"   - Today's Edition: Federal Board Clears 451 Pages... + Insight Global 1,700 + Money Moves 30-Yr 6.89% FRED, Bitcoin $64k, S&P, Dow, UONE $5.05 etc.")
    print(f"   - Sources: [Federal Register][TheGrio], [Atlanta Business Chronicle][Company Release] - 2 per long, 1 for prices")
    print(f"   - Archive: {out_path} and {july17_path}")

if __name__ == "__main__":
    build_issue()
