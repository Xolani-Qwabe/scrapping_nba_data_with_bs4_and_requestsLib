import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.basketball-reference.com/boxscores/202310240DEN.html'


def get_page_data(url):
    data_source = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    return BeautifulSoup(data_source.content, 'html.parser')


page = get_page_data(url)
# %%
tables = page.find_all('table')
basic_team_A = tables[0]
advanced_team_A = tables[7]
basic_team_H = tables[8]
advanced_team_H = tables[15]


# %%
def get_game_details(page):
    details = page.find(id='content').find('h1').get_text()
    return details.replace(' ', '').replace(',', '_')


game_details = get_game_details(page)
game_details


# %%
def get_basic_table_headers(table):
    return [th.getText().split('\n') for th in table.find_all('tr', limit=5)[1:2]][0][1:-1]


# %%

# %%
def get_Basic_table_rows(table):
    return [td for td in table.find('tbody').find_all('tr')]


# %%
def get_basic_table_data(rows):
    player_stats = [[td.getText() for td in rows[i].find_all('td')] for i in range(len(rows))]
    player_names = [[td.getText() for td in rows[i].find_all('a')] for i in range(len(rows))]
    return player_names, player_stats


# %%
def make_basic_table_rows(player_names, player_stats):
    player_names[5].insert(5, 'player')
    for i in range(len(player_names)):
        player = player_names[i][0]
        (player_stats[i].insert(0, player))


def make_basic_table_pandas(basic_table):
    basic_table_player_names, basic_table_player_stats = get_basic_table_data(rows=get_Basic_table_rows(basic_table))
    headers = get_basic_table_headers(basic_table)
    make_basic_table_rows(basic_table_player_names, basic_table_player_stats)
    return pd.DataFrame(basic_table_player_stats, columns=headers)


basic_table_home = make_basic_table_pandas(basic_team_H)
basic_table_away = make_basic_table_pandas(basic_team_A)

print(basic_table_away)
print(basic_table_home)