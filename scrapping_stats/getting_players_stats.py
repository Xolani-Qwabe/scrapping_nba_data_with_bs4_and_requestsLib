import requests
from bs4 import BeautifulSoup
import pandas as pd
import clevercsv


url = 'https://www.basketball-reference.com/leagues/NBA_2024_per_game.html'
data_source = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
page = BeautifulSoup(data_source.content, 'html.parser')



headers = [th.getText().split('\n') for th in page.find_all('tr',limit=1)][0][2:-1]

data_rows = page.find_all('tr')[1:]

player_stats = [[td.getText() for td in data_rows[i].find_all('td')]for i in range(len(data_rows))]

number_of_entries = len(player_stats)
print(number_of_entries)

stats = pd.DataFrame(player_stats, columns=headers)
print(stats)
pd.DataFrame.to_csv(stats,r'C:\Users\thabi\Desktop\scrapping_nba_data_with_bs4_and_requestsLib\nba_stats_per_game.csv')
