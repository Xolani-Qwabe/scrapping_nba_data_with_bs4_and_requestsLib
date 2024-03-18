import re
import sqlite3
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def get_bs4_table_by_id(link, table_id):
    driver = webdriver.Firefox()
    driver.get(link)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, 'content'))
    )
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    content_div = soup.find('div', id='content')
    table = content_div.find('table', id=table_id)
    return table


schedule_schema = '''CREATE TABLE IF NOT EXISTS schedule 
(date TEXT,start_time TEXT,away TEXT,away_score TEXT, home TEXT,
home_score TEXT, boxscore_links_for_the_day TEXT, '' TEXT,
attendance TEXT, arena TEXT, plus_minus_per_100_on_court TEXT,
plus_minus_per_100_off_court TEXT, turnover_bad_pass TEXT, turnover_lost_ball TEXT,
shooting_fouls TEXT, offensive_fouls TEXT,shooting_fouls_drawn TEXT, offensive_fouls_drawn TEXT,
points_generated_by_assist TEXT, and_1_fg TEXT, blocked_fg TEXT)'''


def get_html_table_data(html_table, base_url='https://www.basketball-reference.com/'):
    data = []
    for row in html_table.find_all('tr'):
        cols = row.find_all(['th', 'td'])
        cols_data = [col.text.strip() for col in cols]

        # Extract link if it exists
        link = row.find('a')

        link_href = link['href'] if link else None
        # print(link_href)
        # Join the link with the base_url to get the full URL
        full_link = urljoin(base_url, link_href) if link_href else None

        # Replace "Box Score" with the link URL
        if "Box Score" in cols_data:
            cols_data[cols_data.index("Box Score")] = full_link


        # Exclude rows with 'Did Not Play' status
        if 'Did Not Play' not in cols_data:
            data.append(cols_data)
    return data

oct = 'https://www.basketball-reference.com/leagues/NBA_2024_games.html'
nov = 'https://www.basketball-reference.com/leagues/NBA_2024_games-november.html'
dec = 'https://www.basketball-reference.com/leagues/NBA_2024_games-december.html'
jan ='https://www.basketball-reference.com/leagues/NBA_2024_games-january.html'
feb = 'https://www.basketball-reference.com/leagues/NBA_2024_games-february.html'
mar = 'https://www.basketball-reference.com/leagues/NBA_2024_games-march.html'

table = get_bs4_table_by_id('https://www.basketball-reference.com/leagues/NBA_2024_games.html', 'schedule')


data = get_html_table_data(table)



def create_game_id(date, home_team, away_team):
    # Extract month, day, and year from the date string
    match = re.match(r'^\w{3}, (\w{3}) (\d{2}), (\d{4})$', date)
    month, day, year = match.groups()

    # Convert month abbreviation to a numerical value (e.g., Oct -> 10)
    month_dict = {
        'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
        'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
        'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
    }
    month = month_dict[month]

    # Replace spaces in team names with underscores and convert to lowercase
    home_team = home_team.lower().replace(' ', '_')
    away_team = away_team.lower().replace(' ', '_')

    # Construct the game ID using the format: YYYYMMDD_homeTeam_awayTeam
    game_id = f"{year}{month}{day}_{home_team}_{away_team}"

    return game_id

home = data[1][4]
away = data[1][2]
date = data[1][0]

g_id = create_game_id(date,home,away)

print(g_id)