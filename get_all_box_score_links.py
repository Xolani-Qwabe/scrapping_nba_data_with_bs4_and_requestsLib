import requests
from bs4 import BeautifulSoup
import time


oct_url = 'https://www.basketball-reference.com/leagues/NBA_2024_games.html'
nov_url = 'https://www.basketball-reference.com/leagues/NBA_2024_games-november.html'
dec_url = 'https://www.basketball-reference.com/leagues/NBA_2024_games-december.html'
jan_url = 'https://www.basketball-reference.com/leagues/NBA_2024_games-january.html'
feb_url = 'https://www.basketball-reference.com/leagues/NBA_2024_games-february.html'
all_box_score_links = [oct_url,nov_url,dec_url,jan_url,feb_url]

def get_page(url):
    data_source = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    return BeautifulSoup(data_source.content, 'html.parser')


# this will get all the (<a>) links that ends with .html
# and starts with /boxscores, get href values and return a list.
def get_all_box_score_links(page):
    a_elements = page.find_all('a', href=lambda href: href.endswith('.html') and href.startswith('/boxscores'))
    ref = 'href'
    return [f'https://www.basketball-reference.com{a_element.get(ref)}' for a_element in a_elements]




def list_all_box_score_2024_games(urls):
    all = []
    for url in urls:
        list = get_all_box_score_links(get_page(url))
        all += list
        time.sleep(2)
    return all

links = list_all_box_score_2024_games(all_box_score_links)
print(links)
