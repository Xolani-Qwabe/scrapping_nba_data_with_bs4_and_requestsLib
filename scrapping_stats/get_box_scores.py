import requests
from bs4 import BeautifulSoup
import pandas as pd
import get_all_box_score_links
import time
import regex as r
from datetime import datetime


def get_html_page(url):
    response = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0'
    },)
    time.sleep(5)
    return BeautifulSoup(response.content, 'html.parser')


def get_html_pages(links):
    pages = []
    for link in links:
        response = requests.get(link, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0'
        },)
        time.sleep(3)
        pages.append(BeautifulSoup(response.content, 'html.parser'))
    return pages


# returns a list/tuple with basic_home_table, advanced_home_table, basic_away_table, advanced_away_table
def get_tables(page):
    tables = page.find_all('table')
    return tables[8],tables[15],tables[0],tables[7]


# finds the header with #id content and grabs the inner text
def get_game_details(page):
    return page.find(id='content').find('h1').get_text()


def get_game_details_for_table(page):
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


def make_basic_table_pandas(basic_table,page):
    rows = get_table_rows(basic_table)
    player_names, player_stats = get_table_data(rows)
    get_game_details = get_game_details_for_table(page)
    away, home, date = get_game_info_list(get_game_details)
    [player_stat.append(away) for player_stat in player_stats]
    [player_stat.append(home) for player_stat in player_stats]
    [player_stat.append(date) for player_stat in player_stats]
    headers = get_advanced_table_headers(basic_table)
    headers.append("Away")
    headers.append("Home")
    headers.append("Date")
    make_table_rows(player_names, player_stats)
    df = pd.DataFrame(player_stats, columns=headers)
    df.fillna(0.0, inplace=True)
    df.replace('Did Not Play', '0:0', inplace=True)
    df.drop(5, inplace=True)
    return df


def make_advanced_table_pandas(adv_table,page):
    rows = get_table_rows(adv_table)
    player_names, player_stats = get_table_data(rows)
    get_game_details = get_game_details_for_table(page)
    away, home, date = get_game_info_list(get_game_details)
    [player_stat.append(away) for player_stat in player_stats]
    [player_stat.append(home) for player_stat in player_stats]
    [player_stat.append(date) for player_stat in player_stats]
    headers = get_advanced_table_headers(adv_table)
    headers.append("Away",)
    headers.append("Home")
    headers.append("Date")
    make_table_rows(player_names, player_stats)
    df = pd.DataFrame(player_stats, columns=headers)
    df.fillna(0.0, inplace=True)
    df.replace('Did Not Play', '0:0', inplace=True)
    df.drop(5, inplace=True)
    return df


def write_basic_tables_to_file(details, basic_table_home, basic_table_away):
    path = '../reading_cleaning_data/box_score_tables_csv'
    home_path = f'{path}/basic_table_H_{details}.csv'
    away_path = f'{path}/basic_table_A_{details}.csv'
    pd.DataFrame.to_csv(basic_table_home, home_path)
    pd.DataFrame.to_csv(basic_table_away, away_path)


def write_advanced_tables_to_file(details, adv_table_home, adv_table_away):
    path = '../reading_cleaning_data/box_score_tables_csv'
    home_path = f'{path}/advanced_table_H_{details}.csv'
    away_path = f'{path}/advanced_table_A_{details}.csv'
    pd.DataFrame.to_csv(adv_table_home, home_path)
    pd.DataFrame.to_csv(adv_table_away, away_path)


def tables_to_csv(page):
    print('building tables with pandas')
    basic_table_home = make_basic_table_pandas(get_tables(page)[0],page)
    basic_table_away = make_basic_table_pandas(get_tables(page)[2],page)
    adv_table_away = make_advanced_table_pandas(get_tables(page)[1],page)
    adv_table_home = make_advanced_table_pandas(get_tables(page)[3],page)
    print(basic_table_home)
    game_details = get_game_details(page)
    print(game_details)
    write_basic_tables_to_file(game_details, basic_table_home, basic_table_away)
    write_advanced_tables_to_file(game_details, adv_table_home, adv_table_away)


def get_all_box_score_pages(links):
    pages = map(get_html_pages,links)
    print('fetched pages')
    return pages


def write_all_box_score_pages_to_csv():
    print('Getting HTML pages *********************************************')
    # links = list(get_all_box_score_links.all_box_score_links_2024_games())
    links = [ 'https://www.basketball-reference.com/boxscores/202402030CHI.html', 'https://www.basketball-reference.com/boxscores/202402030DAL.html', 'https://www.basketball-reference.com/boxscores/202402030NYK.html', 'https://www.basketball-reference.com/boxscores/202402030SAS.html', 'https://www.basketball-reference.com/boxscores/202402040DET.html', 'https://www.basketball-reference.com/boxscores/202402040WAS.html', 'https://www.basketball-reference.com/boxscores/202402040BOS.html', 'https://www.basketball-reference.com/boxscores/202402040CHO.html', 'https://www.basketball-reference.com/boxscores/202402040MIA.html', 'https://www.basketball-reference.com/boxscores/202402040MIN.html', 'https://www.basketball-reference.com/boxscores/202402040OKC.html', 'https://www.basketball-reference.com/boxscores/202402040UTA.html', 'https://www.basketball-reference.com/boxscores/202402040DEN.html', 'https://www.basketball-reference.com/boxscores/202402050CHO.html', 'https://www.basketball-reference.com/boxscores/202402050CLE.html', 'https://www.basketball-reference.com/boxscores/202402050PHI.html', 'https://www.basketball-reference.com/boxscores/202402050ATL.html', 'https://www.basketball-reference.com/boxscores/202402050BRK.html', 'https://www.basketball-reference.com/boxscores/202402050NOP.html', 'https://www.basketball-reference.com/boxscores/202402060IND.html', 'https://www.basketball-reference.com/boxscores/202402060BRK.html', 'https://www.basketball-reference.com/boxscores/202402060MIA.html', 'https://www.basketball-reference.com/boxscores/202402060NYK.html', 'https://www.basketball-reference.com/boxscores/202402060CHI.html', 'https://www.basketball-reference.com/boxscores/202402060UTA.html', 'https://www.basketball-reference.com/boxscores/202402060PHO.html', 'https://www.basketball-reference.com/boxscores/202402070CHO.html', 'https://www.basketball-reference.com/boxscores/202402070WAS.html', 'https://www.basketball-reference.com/boxscores/202402070BOS.html', 'https://www.basketball-reference.com/boxscores/202402070MIA.html', 'https://www.basketball-reference.com/boxscores/202402070PHI.html', 'https://www.basketball-reference.com/boxscores/202402070LAC.html', 'https://www.basketball-reference.com/boxscores/202402070SAC.html', 'https://www.basketball-reference.com/boxscores/202402080IND.html', 'https://www.basketball-reference.com/boxscores/202402080ORL.html', 'https://www.basketball-reference.com/boxscores/202402080BRK.html', 'https://www.basketball-reference.com/boxscores/202402080NYK.html', 'https://www.basketball-reference.com/boxscores/202402080MEM.html', 'https://www.basketball-reference.com/boxscores/202402080MIL.html', 'https://www.basketball-reference.com/boxscores/202402080PHO.html', 'https://www.basketball-reference.com/boxscores/202402080LAL.html', 'https://www.basketball-reference.com/boxscores/202402080POR.html', 'https://www.basketball-reference.com/boxscores/202402090PHI.html', 'https://www.basketball-reference.com/boxscores/202402090BOS.html', 'https://www.basketball-reference.com/boxscores/202402090TOR.html', 'https://www.basketball-reference.com/boxscores/202402090MIL.html', 'https://www.basketball-reference.com/boxscores/202402090SAC.html', 'https://www.basketball-reference.com/boxscores/202402090LAL.html', 'https://www.basketball-reference.com/boxscores/202402100DAL.html', 'https://www.basketball-reference.com/boxscores/202402100LAC.html', 'https://www.basketball-reference.com/boxscores/202402100BRK.html', 'https://www.basketball-reference.com/boxscores/202402100CHO.html', 'https://www.basketball-reference.com/boxscores/202402100ORL.html', 'https://www.basketball-reference.com/boxscores/202402100WAS.html', 'https://www.basketball-reference.com/boxscores/202402100ATL.html', 'https://www.basketball-reference.com/boxscores/202402100NYK.html', 'https://www.basketball-reference.com/boxscores/202402100TOR.html', 'https://www.basketball-reference.com/boxscores/202402100GSW.html', 'https://www.basketball-reference.com/boxscores/202402100POR.html', 'https://www.basketball-reference.com/boxscores/202402110MIA.html', 'https://www.basketball-reference.com/boxscores/202402110OKC.html', 'https://www.basketball-reference.com/boxscores/202402120CHO.html', 'https://www.basketball-reference.com/boxscores/202402120CLE.html', 'https://www.basketball-reference.com/boxscores/202402120ATL.html', 'https://www.basketball-reference.com/boxscores/202402120TOR.html', 'https://www.basketball-reference.com/boxscores/202402120HOU.html', 'https://www.basketball-reference.com/boxscores/202402120MEM.html', 'https://www.basketball-reference.com/boxscores/202402120MIL.html', 'https://www.basketball-reference.com/boxscores/202402120DAL.html', 'https://www.basketball-reference.com/boxscores/202402120UTA.html', 'https://www.basketball-reference.com/boxscores/202402120LAC.html', 'https://www.basketball-reference.com/boxscores/202402130BRK.html', 'https://www.basketball-reference.com/boxscores/202402130ORL.html', 'https://www.basketball-reference.com/boxscores/202402130MIL.html', 'https://www.basketball-reference.com/boxscores/202402130PHO.html', 'https://www.basketball-reference.com/boxscores/202402130POR.html', 'https://www.basketball-reference.com/boxscores/202402130LAL.html', 'https://www.basketball-reference.com/boxscores/202402140CHO.html', 'https://www.basketball-reference.com/boxscores/202402140ORL.html', 'https://www.basketball-reference.com/boxscores/202402140PHI.html', 'https://www.basketball-reference.com/boxscores/202402140BOS.html', 'https://www.basketball-reference.com/boxscores/202402140CLE.html', 'https://www.basketball-reference.com/boxscores/202402140TOR.html', 'https://www.basketball-reference.com/boxscores/202402140MEM.html', 'https://www.basketball-reference.com/boxscores/202402140NOP.html', 'https://www.basketball-reference.com/boxscores/202402140DAL.html', 'https://www.basketball-reference.com/boxscores/202402140DEN.html', 'https://www.basketball-reference.com/boxscores/202402140PHO.html', 'https://www.basketball-reference.com/boxscores/202402140UTA.html', 'https://www.basketball-reference.com/boxscores/202402140GSW.html']
    print(len(links))
    pages = [get_html_page(url) for url in links]
    [tables_to_csv(page) for page in pages]


def get_game_info_list(game_string):
    # Regular expression pattern to extract game details, team names, and date
    pattern = r'(?:In-SeasonTournamentFinal:)?([A-Z][a-z0-9]+(?:[A-Z][a-z0-9]+)*)at([A-Z][a-z0-9]+(?:[A-Z][a-z0-9]+)*)BoxScore_(\w+\d+_\d+)'
    # Extracting information from each string
    match = r.match(pattern, game_string)
    if match:
        team1 = match.group(1)
        team2 = match.group(2)
        date = match.group(3)
        # Insert spaces between camel case team names
        team1 = r.sub(r"(?<=\w)([A-Z])", r" \1", team1)
        team2 = r.sub(r"(?<=\w)([A-Z])", r" \1", team2)
        date_obj = datetime.strptime(date, '%B%d_%Y')
        formatted_date = date_obj.strftime('%Y-%m-%d')
        print("Game:", team1, "at", team2)
        print("Date:", formatted_date)
        return [team1, team2, formatted_date]
    else:
        print("No match found for:", game_string)


if __name__ == '__main__':
   write_all_box_score_pages_to_csv()

