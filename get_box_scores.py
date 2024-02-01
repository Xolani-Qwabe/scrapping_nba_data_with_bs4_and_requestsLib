import requests
from bs4 import BeautifulSoup
import pandas as pd
#%%
url = 'https://www.basketball-reference.com/boxscores/202310240DEN.html'
data_source = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
page = BeautifulSoup(data_source.content, 'html.parser')
#%%
headers =[th.getText().split('\n') for th in page.find_all('tr',limit=5)[1:2]][0][1:-1]

table_body = page.find('tbody').find_all('tr', limit=5)
#%%
rows = [td for td in page.find('tbody').find_all('tr')]
#%%
player_names = [[td.getText() for td in rows[i].find_all('a')]for i in range(len(rows))]
#%%
player_stats = [[td.getText() for td in rows[i].find_all('td')]for i in range(len(rows))]



def make_rows(player_names, player_stats):
    player_names[5].insert(5, 'player')
    for i in range(len(player_names)):
        player = player_names[i][0]
        (player_stats[i].insert(0,player))

make_rows(player_names, player_stats)

stats = pd.DataFrame(player_stats, columns=headers)
