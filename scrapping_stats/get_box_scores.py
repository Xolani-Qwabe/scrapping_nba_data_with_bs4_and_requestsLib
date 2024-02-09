import requests
from bs4 import BeautifulSoup
import pandas as pd
import get_all_box_score_links
import time




def get_page_data(url):
    response = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0'
    },timeout= 2)
    time.sleep(5)
    return BeautifulSoup(response.content, 'html.parser')

def get_html_pages(links):
    pages = []
    for link in links:
        response = requests.get(link, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0'
        }, timeout=10)
        time.sleep(20)
        pages.append(BeautifulSoup(response.content, 'html.parser'))
    return pages



# returns a list/tuple with basic_home_table, advanced_home_table, basic_away_table, advanced_away_table
def get_tables(page):
    tables = page.find_all('table')
    return tables[8],tables[15],tables[0],tables[7]


def get_game_details(page):
    details = page.find(id='content').find('h1').get_text()
    return details.replace(' ', '').replace(',', '_')


def get_basic_table_headers(table):
    return [th.getText().split('\n') for th in table.find_all('tr', limit=5)[1:2]][0][1:-1]


def get_advanced_table_headers(table):
    headers = [th.getText().split('\n') for th in table.find_all('tr')[1]]
    clean = [header for header in headers if header != ['', '']]
    return [item for new_array in clean for item in new_array]



def get_table_rows(table):
    return [td for td in table.find('tbody').find_all('tr')]




def get_table_data(rows):
    player_stats = [[td.getText() for td in rows[i].find_all('td')] for i in range(len(rows))]
    player_names = [[td.getText() for td in rows[i].find_all('a')] for i in range(len(rows))]
    return player_names, player_stats


def make_table_rows(player_names, player_stats):
    player_names[5].insert(5, 'player')
    for i in range(len(player_names)):
        player = player_names[i][0]
        (player_stats[i].insert(0, player))


def make_basic_table_pandas(basic_table):
    player_names, player_stats = get_table_data(rows=get_table_rows(basic_table))
    headers = get_basic_table_headers(basic_table)
    make_table_rows(player_names, player_stats)
    return pd.DataFrame(player_stats, columns=headers)


def make_advanced_table_pandas(adv_table):
    player_names, player_stats = get_table_data(rows=get_table_rows(adv_table))
    headers = get_advanced_table_headers(adv_table)
    make_table_rows(player_names, player_stats)
    return pd.DataFrame(player_stats, columns=headers)

def write_basic_tables_to_file(details, basic_table_home, basic_table_away):
    path = '../box_score_tables_csv'
    home_path = f'{path}/basic_table_H_{details}.csv'
    away_path = f'{path}/basic_table_A_{details}.csv'
    pd.DataFrame.to_csv(basic_table_home, home_path)
    pd.DataFrame.to_csv(basic_table_away, away_path)


def write_advanced_tables_to_file(details, adv_table_home, adv_table_away):
    path = '../box_score_tables_csv'
    home_path = f'{path}/advanced_table_H_{details}.csv'
    away_path = f'{path}/advanced_table_A_{details}.csv'
    pd.DataFrame.to_csv(adv_table_home, home_path)
    pd.DataFrame.to_csv(adv_table_away, away_path)



def tables_to_csv(page):
    basic_table_home = make_basic_table_pandas(get_tables(page)[0])
    basic_table_away = make_basic_table_pandas(get_tables(page)[2])
    adv_table_away = (make_advanced_table_pandas(get_tables(page)[1]))
    adv_table_home = (make_advanced_table_pandas(get_tables(page)[3]))
    game_details = get_game_details(page)
    write_basic_tables_to_file(game_details, basic_table_home, basic_table_away)
    write_advanced_tables_to_file(game_details, adv_table_home, adv_table_away)

def get_all_box_score_pages(links):
    pages = map(get_page_data,links)
    print(list(pages))
    print('I am here')
    return pages

def write_all_box_score_pages_to_csv():
    links = ['https://www.basketball-reference.com/boxscores/202311080BRK.html', 'https://www.basketball-reference.com/boxscores/202311080NYK.html', 'https://www.basketball-reference.com/boxscores/202311080CHI.html', 'https://www.basketball-reference.com/boxscores/202311080HOU.html', 'https://www.basketball-reference.com/boxscores/202311080MEM.html', 'https://www.basketball-reference.com/boxscores/202311080MIL.html', 'https://www.basketball-reference.com/boxscores/202311080MIN.html', 'https://www.basketball-reference.com/boxscores/202311080OKC.html', 'https://www.basketball-reference.com/boxscores/202311080DAL.html', 'https://www.basketball-reference.com/boxscores/202311080DEN.html', 'https://www.basketball-reference.com/boxscores/202311080SAC.html', 'https://www.basketball-reference.com/boxscores/202311090IND.html', 'https://www.basketball-reference.com/boxscores/202311090ORL.html', 'https://www.basketball-reference.com/boxscores/202311100DET.html', 'https://www.basketball-reference.com/boxscores/202311100WAS.html', 'https://www.basketball-reference.com/boxscores/202311100BOS.html', 'https://www.basketball-reference.com/boxscores/202311100HOU.html', 'https://www.basketball-reference.com/boxscores/202311100MEM.html', 'https://www.basketball-reference.com/boxscores/202311100SAS.html', 'https://www.basketball-reference.com/boxscores/202311100DAL.html', 'https://www.basketball-reference.com/boxscores/202311100PHO.html', 'https://www.basketball-reference.com/boxscores/202311100SAC.html', 'https://www.basketball-reference.com/boxscores/202311110ORL.html', 'https://www.basketball-reference.com/boxscores/202311110BOS.html', 'https://www.basketball-reference.com/boxscores/202311110ATL.html', 'https://www.basketball-reference.com/boxscores/202311110GSW.html', 'https://www.basketball-reference.com/boxscores/202311120NYK.html', 'https://www.basketball-reference.com/boxscores/202311120BRK.html', 'https://www.basketball-reference.com/boxscores/202311120LAC.html', 'https://www.basketball-reference.com/boxscores/202311120PHI.html', 'https://www.basketball-reference.com/boxscores/202311120CHI.html', 'https://www.basketball-reference.com/boxscores/202311120HOU.html']
    pages = list(get_html_pages(links))
    print(pages)
    map(tables_to_csv, pages)

if __name__ == '__main__':
    # url = 'https://www.basketball-reference.com/boxscores/202311080PHI.html'
    write_all_box_score_pages_to_csv()
    # page = get_page_data(url)
    # tables_to_csv(page)