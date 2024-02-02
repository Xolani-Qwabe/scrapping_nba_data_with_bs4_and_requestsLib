import requests
from bs4 import BeautifulSoup
import time

#%%
oct_url = 'https://www.basketball-reference.com/leagues/NBA_2024_games.html'
nov_url = 'https://www.basketball-reference.com/leagues/NBA_2024_games-november.html'
dec_url = 'https://www.basketball-reference.com/leagues/NBA_2024_games-december.html'
jan_url = 'https://www.basketball-reference.com/leagues/NBA_2024_games-january.html'
feb_url = 'https://www.basketball-reference.com/leagues/NBA_2024_games-february.html'
def get_page(url):
    data_source = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    return BeautifulSoup(data_source.content, 'html.parser')


# this will get all the (<a>) links that ends with .html
# and starts with /boxscores, get href values and return a list.
def get_all_box_score_links(page):
    a_elements = page.find_all('a', href=lambda href: href.endswith('.html') and href.startswith('/boxscores'))
    return [a_element.get('href') for a_element in a_elements]

print(get_all_box_score_links(get_page(oct_url)))
time.sleep(5)
print(get_all_box_score_links(get_page(nov_url)))
time.sleep(5)
print(get_all_box_score_links(get_page(dec_url)))
time.sleep(5)
print(get_all_box_score_links(get_page(jan_url)))
time.sleep(5)
print(get_all_box_score_links(get_page(feb_url)))
time.sleep(5)