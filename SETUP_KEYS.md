
# Add Live Keys - Do this now for tomorrow 6am live

GitHub > Your Repo > Settings > Secrets and variables > Actions > New repository secret

1. FRED_API_KEY
   - Get free: https://fred.stlouisfed.org/docs/api/api_key.html
   - Sign up, get key, add as secret FRED_API_KEY
   - This makes 30-Yr Mortgage LIVE from Federal Reserve

2. FINNHUB_API_KEY
   - Get free: https://finnhub.io/register
   - Free tier: 60 calls/min, enough for daily
   - Add as secret FINNHUB_API_KEY
   - This makes Black Wall Street Watch LIVE:
     - UONE (Urban One)
     - RLJ (RLJ Lodging Trust)
     - CARV (Carver Bancorp)
     - S&P 500 via SPY
     - Dow via DIA

CoinGecko BTC/ETH is already live, no key needed.

After adding secrets, run Actions > Run workflow manually to test live data now.
Tomorrow 6am ET it will auto-run with live data.
