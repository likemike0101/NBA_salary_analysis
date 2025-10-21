import time
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; research/1.0; +https://example.com/contact)"
}

def clean_money(x):
    if pd.isna(x):
        return None
    s = re.sub(r"[$,]", "", str(x)).strip()
    try:
        return int(float(s))
    except ValueError:
        return None

def scrape_team_salary_page(url, pause=1.5):
    """Parse a HoopsHype-like salary table into a clean DataFrame."""
    time.sleep(pause)
    r = requests.get(url, headers=HEADERS, timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")

    # Find the main table (inspect page to confirm the selector)
    table = soup.find("table")
    if table is None:
        return pd.DataFrame()

    # Extract headers
    headers = [th.get_text(strip=True) for th in table.find_all("th")]
    rows = []
    for tr in table.find_all("tr"):
        tds = tr.find_all(["td"])
        if not tds:
            continue
        row = [td.get_text(strip=True) for td in tds]
        # If there are links for player/team names, you can also capture hrefs:
        # link = tds[0].find("a")
        # player_url = link["href"] if link else None
        rows.append(row)

    df = pd.DataFrame(rows, columns=headers[:len(rows[0])])  # align col count
    df["source_url"] = url

    # Example cleaning: normalize currency columns
    money_cols = [c for c in df.columns if "Salary" in c or "Cap" in c or "Total" in c]
    for c in money_cols:
        df[c + "_num"] = df[c].apply(clean_money)

    # Example cleaning: strip footnote asterisks from names
    if "Player" in df.columns:
        df["Player"] = df["Player"].str.replace(r"\*$", "", regex=True)

    return df

# Example usage
# url = "https://hoopshype.com/salaries/teams/detroit_pistons/"
# pistons = scrape_team_salary_page(url)
# print(pistons.head())