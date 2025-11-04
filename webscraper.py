import pandas as pd
import re
import requests


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15"
}

NBA_TEAM_URL = {
    "Atlanta Hawks": "https://www.hoopshype.com/salaries/teams/atlanta-hawks/1/?season=",
    "Boston Celtics": "https://www.hoopshype.com/salaries/teams/boston-celtics/2/?season=",
    "Brooklyn Nets": "https://www.hoopshype.com/salaries/teams/brooklyn-nets/17/?season=",
    "Charlotte Hornets": "https://www.hoopshype.com/salaries/teams/charlotte-hornets/5312/?season=",
    "Chicago Bulls": "https://www.hoopshype.com/salaries/teams/chicago-bulls/4/?season=",
    "Cleveland Cavaliers": "https://www.hoopshype.com/salaries/teams/cleveland-cavaliers/5/?season=",
    "Dallas Mavericks": "https://www.hoopshype.com/salaries/teams/dallas-mavericks/6/?season=",
    "Denver Nuggets": "https://www.hoopshype.com/salaries/teams/denver-nuggets/7/?season=",
    "Detroit Pistons": "https://www.hoopshype.com/salaries/teams/detroit-pistons/8/?season=",
    "Golden State Warriors": "https://www.hoopshype.com/salaries/teams/golden-state-warriors/9/?season=",
    "Houston Rockets": "https://www.hoopshype.com/salaries/teams/houston-rockets/10/?season=",
    "Indiana Pacers": "https://www.hoopshype.com/salaries/teams/indiana-pacers/11/?season=",
    "Los Angeles Clippers": "https://www.hoopshype.com/salaries/teams/los-angeles-clippers/12/?season=",
    "Los Angeles Lakers": "https://www.hoopshype.com/salaries/teams/los-angeles-lakers/13/?season=",
    "Memphis Grizzlies": "https://www.hoopshype.com/salaries/teams/memphis-grizzlies/29/?season=",
    "Miami Heat": "https://www.hoopshype.com/salaries/teams/miami-heat/14/?season=",
    "Milwaukee Bucks": "https://www.hoopshype.com/salaries/teams/milwaukee-bucks/15/?season=",
    "Minnesota Timberwolves": "https://www.hoopshype.com/salaries/teams/minnesota-timberwolves/16/?season=",
    "New Orleans Pelicans": "https://www.hoopshype.com/salaries/teams/new-orleans-pelicans/3/?season=",
    "New York Knicks": "https://www.hoopshype.com/salaries/teams/new-york-knicks/18/?season=",
    "Oklahoma City Thunder": "https://www.hoopshype.com/salaries/teams/oklahoma-city-thunder/25/?season=",
    "Orlando Magic": "https://www.hoopshype.com/salaries/teams/orlando-magic/19/?season=",
    "Philadelphia 76ers": "https://www.hoopshype.com/salaries/teams/philadelphia-76ers/20/?season=",
    "Phoenix Suns": "https://www.hoopshype.com/salaries/teams/phoenix-suns/21/?season=",
    "Portland Trail Blazers": "https://www.hoopshype.com/salaries/teams/portland-trail-blazers/22/?season=",
    "Sacramento Kings": "https://www.hoopshype.com/salaries/teams/sacramento-kings/23/?season=",
    "San Antonio Spurs": "https://www.hoopshype.com/salaries/teams/san-antonio-spurs/24/?season=",
    "Toronto Raptors": "https://www.hoopshype.com/salaries/teams/toronto-raptors/28/?season=",
    "Utah Jazz": "https://www.hoopshype.com/salaries/teams/utah-jazz/26/?season=",
    "Washington Wizards": "https://www.hoopshype.com/salaries/teams/washington-wizards/27/?season="
}

def fetch_team_table(url: str) -> pd.DataFrame:
    """Fetch the salaries table HTML with headers, then parse via pandas."""
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    tables = pd.read_html(resp.text)
    if not tables:
        raise ValueError("No tables found on page")
    df = tables[0].copy()

    # Drop first column if it's the rank column (often unnamed or 'Rk')
    if df.columns[0] in ('Unnamed: 0', df.columns[0]) and df.shape[1] >= 2:
        df = df.drop(columns=[df.columns[0]])
    # Keep only first 2 columns (name + current season)
    df = df.iloc[:, :2]
    df.columns = ['player', 'salary_raw']

    # Drop the 'Total' row and any NaNs
    df = df[df['player'].astype(str).str.lower() != 'total'].dropna(subset=['player'])

    return df.reset_index(drop=True)

_money_pat = re.compile(r'[\d,]+(?:\.\d+)?')  # picks up numbers inside "$xx,xxx" or "TW$xxx bruh
def parse_salary_to_float(s: str) -> float:
    """Extract numeric dollars from strings like '$43,031,940' or 'TW$578,577' or '$186,594'."""
    if pd.isna(s):
        return float('nan')
    s = str(s)
    m = _money_pat.search(s.replace('\xa0', ' '))
    if not m:
        return float('nan')
    return float(m.group(0).replace(',', ''))


def scrape_team(team: str, base_url: str, season: int) -> pd.DataFrame:
    df = fetch_team_table(f"{base_url}{season}")
    df['salary'] = df['salary_raw'].map(parse_salary_to_float)
    # Sort highest paid first; keep only rows with a valid salary number
    df = df.dropna(subset=['salary']).sort_values('salary', ascending=False).reset_index(drop=True)
    df['rank'] = df.index + 1
    df['team'] = team
    df['season'] = season
    return df[['team', 'season', 'rank', 'player', 'salary']]

def build_team_season_wide(nba_urls: dict, season: int, top_n: int = 15) -> pd.DataFrame:
    # Collect long-form rows
    long_rows = []
    for team, url in nba_urls.items():
        try:
            team_df = scrape_team(team, url, season)
        except Exception as e:
            print(f"[WARN] {team}: {e}")
            continue
        # Limit to top N
        long_rows.append(team_df.head(top_n))

    if not long_rows:
        raise RuntimeError("No team tables were parsed successfully.")

    long_df = pd.concat(long_rows, ignore_index=True)

    # one row per team-season.
    name_wide = long_df.pivot(index=['team', 'season'], columns='rank', values='player')
    sal_wide  = long_df.pivot(index=['team', 'season'], columns='rank', values='salary')

    # Rename columns
    name_wide.columns = [f"P{r}_name" for r in name_wide.columns]
    sal_wide.columns  = [f"P{r}_salary" for r in sal_wide.columns]

    wide = pd.concat([name_wide, sal_wide], axis=1).reset_index()

    # sort columns 
    # e.g., P1_name, P1_salary, P2_name, P2_salary, …
    def _sort_key(col):
        if col in ('team', 'season'):
            return (-1, col)
        m = re.match(r'P(\d+)_(name|salary)$', col)
        if not m:
            return (9999, col)
        return (int(m.group(1)), 0 if m.group(2) == 'name' else 1)

    wide = wide.reindex(sorted(wide.columns, key=_sort_key), axis=1)
    return wide
TOP_N = 15      # change this if you want more/fewer columns

for i in range(2020, 2025):
    season = i
    team_season_wide = build_team_season_wide(NBA_TEAM_URL, season=season, top_n=TOP_N)


    pd.set_option('display.max_columns', None)
    print(team_season_wide.head(3))
    team_season_wide.to_csv(f"nba_salaries_top{TOP_N}_{season}.csv", index=False)