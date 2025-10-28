import pandas as pd


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
temp_url = NBA_TEAM_URL['Atlanta Hawks'] + "2024"
tables = pd.read_html(temp_url)

df = tables[0]


df.columns = ['index', 'player', '2024-2025']

print(df)