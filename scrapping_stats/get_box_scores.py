import requests
from bs4 import BeautifulSoup
import pandas as pd
import get_all_box_score_links
import time




def get_page_data(url):
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
        time.sleep(10)
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
    print('building tables with pandas')
    basic_table_home = make_basic_table_pandas(get_tables(page)[0])
    basic_table_away = make_basic_table_pandas(get_tables(page)[2])
    adv_table_away = (make_advanced_table_pandas(get_tables(page)[1]))
    adv_table_home = (make_advanced_table_pandas(get_tables(page)[3]))
    print(basic_table_home)
    game_details = get_game_details(page)
    write_basic_tables_to_file(game_details, basic_table_home, basic_table_away)
    write_advanced_tables_to_file(game_details, adv_table_home, adv_table_away)

def get_all_box_score_pages(links):
    pages = map(get_page_data,links)
    # print(list(pages))
    print('fetched pages')
    return pages

def write_all_box_score_pages_to_csv():
    print('Getting HTML pages *********************************************')
    links = ['https://www.basketball-reference.com/boxscores/202312110CHO.html', 'https://www.basketball-reference.com/boxscores/202312110DET.html', 'https://www.basketball-reference.com/boxscores/202312110ORL.html', 'https://www.basketball-reference.com/boxscores/202312110PHI.html', 'https://www.basketball-reference.com/boxscores/202312110ATL.html', 'https://www.basketball-reference.com/boxscores/202312110NYK.html', 'https://www.basketball-reference.com/boxscores/202312110HOU.html', 'https://www.basketball-reference.com/boxscores/202312110MEM.html', 'https://www.basketball-reference.com/boxscores/202312110MIL.html', 'https://www.basketball-reference.com/boxscores/202312110NOP.html', 'https://www.basketball-reference.com/boxscores/202312110OKC.html', 'https://www.basketball-reference.com/boxscores/202312110SAC.html', 'https://www.basketball-reference.com/boxscores/202312110LAC.html', 'https://www.basketball-reference.com/boxscores/202312120BOS.html', 'https://www.basketball-reference.com/boxscores/202312120DAL.html', 'https://www.basketball-reference.com/boxscores/202312120CHI.html', 'https://www.basketball-reference.com/boxscores/202312120PHO.html', 'https://www.basketball-reference.com/boxscores/202312120LAC.html', 'https://www.basketball-reference.com/boxscores/202312130DET.html', 'https://www.basketball-reference.com/boxscores/202312130WAS.html', 'https://www.basketball-reference.com/boxscores/202312130MIA.html', 'https://www.basketball-reference.com/boxscores/202312130TOR.html', 'https://www.basketball-reference.com/boxscores/202312130HOU.html', 'https://www.basketball-reference.com/boxscores/202312130MIL.html', 'https://www.basketball-reference.com/boxscores/202312130SAS.html', 'https://www.basketball-reference.com/boxscores/202312130PHO.html', 'https://www.basketball-reference.com/boxscores/202312130UTA.html', 'https://www.basketball-reference.com/boxscores/202312140BOS.html', 'https://www.basketball-reference.com/boxscores/202312140MIA.html', 'https://www.basketball-reference.com/boxscores/202312140DAL.html', 'https://www.basketball-reference.com/boxscores/202312140DEN.html', 'https://www.basketball-reference.com/boxscores/202312140POR.html', 'https://www.basketball-reference.com/boxscores/202312140SAC.html', 'https://www.basketball-reference.com/boxscores/202312140LAC.html', 'https://www.basketball-reference.com/boxscores/202312150CHO.html', 'https://www.basketball-reference.com/boxscores/202312150PHI.html', 'https://www.basketball-reference.com/boxscores/202312150WAS.html', 'https://www.basketball-reference.com/boxscores/202312150BOS.html', 'https://www.basketball-reference.com/boxscores/202312150SAS.html', 'https://www.basketball-reference.com/boxscores/202312150TOR.html', 'https://www.basketball-reference.com/boxscores/202312150MEM.html', 'https://www.basketball-reference.com/boxscores/202312150PHO.html', 'https://www.basketball-reference.com/boxscores/202312160MIL.html', 'https://www.basketball-reference.com/boxscores/202312160CHO.html', 'https://www.basketball-reference.com/boxscores/202312160CLE.html', 'https://www.basketball-reference.com/boxscores/202312160MIA.html', 'https://www.basketball-reference.com/boxscores/202312160MIN.html', 'https://www.basketball-reference.com/boxscores/202312160GSW.html', 'https://www.basketball-reference.com/boxscores/202312160DEN.html', 'https://www.basketball-reference.com/boxscores/202312160POR.html', 'https://www.basketball-reference.com/boxscores/202312160SAC.html', 'https://www.basketball-reference.com/boxscores/202312160LAC.html', 'https://www.basketball-reference.com/boxscores/202312170BOS.html', 'https://www.basketball-reference.com/boxscores/202312170SAS.html', 'https://www.basketball-reference.com/boxscores/202312170MIL.html', 'https://www.basketball-reference.com/boxscores/202312170PHO.html', 'https://www.basketball-reference.com/boxscores/202312170POR.html', 'https://www.basketball-reference.com/boxscores/202312180CLE.html', 'https://www.basketball-reference.com/boxscores/202312180IND.html', 'https://www.basketball-reference.com/boxscores/202312180PHI.html', 'https://www.basketball-reference.com/boxscores/202312180ATL.html', 'https://www.basketball-reference.com/boxscores/202312180MIA.html', 'https://www.basketball-reference.com/boxscores/202312180TOR.html', 'https://www.basketball-reference.com/boxscores/202312180OKC.html', 'https://www.basketball-reference.com/boxscores/202312180DEN.html', 'https://www.basketball-reference.com/boxscores/202312180UTA.html', 'https://www.basketball-reference.com/boxscores/202312180SAC.html', 'https://www.basketball-reference.com/boxscores/202312180LAL.html', 'https://www.basketball-reference.com/boxscores/202312190NOP.html', 'https://www.basketball-reference.com/boxscores/202312190MIL.html', 'https://www.basketball-reference.com/boxscores/202312190GSW.html', 'https://www.basketball-reference.com/boxscores/202312190POR.html', 'https://www.basketball-reference.com/boxscores/202312200CLE.html', 'https://www.basketball-reference.com/boxscores/202312200IND.html', 'https://www.basketball-reference.com/boxscores/202312200ORL.html', 'https://www.basketball-reference.com/boxscores/202312200PHI.html', 'https://www.basketball-reference.com/boxscores/202312200BRK.html', 'https://www.basketball-reference.com/boxscores/202312200TOR.html', 'https://www.basketball-reference.com/boxscores/202312200CHI.html', 'https://www.basketball-reference.com/boxscores/202312200HOU.html', 'https://www.basketball-reference.com/boxscores/202312200DAL.html', 'https://www.basketball-reference.com/boxscores/202312200SAC.html', 'https://www.basketball-reference.com/boxscores/202312210DET.html', 'https://www.basketball-reference.com/boxscores/202312210CLE.html', 'https://www.basketball-reference.com/boxscores/202312210CHI.html', 'https://www.basketball-reference.com/boxscores/202312210MEM.html', 'https://www.basketball-reference.com/boxscores/202312210MIL.html', 'https://www.basketball-reference.com/boxscores/202312210OKC.html', 'https://www.basketball-reference.com/boxscores/202312210MIN.html', 'https://www.basketball-reference.com/boxscores/202312210POR.html', 'https://www.basketball-reference.com/boxscores/202312220PHI.html', 'https://www.basketball-reference.com/boxscores/202312220BRK.html', 'https://www.basketball-reference.com/boxscores/202312220HOU.html', 'https://www.basketball-reference.com/boxscores/202312220MIA.html', 'https://www.basketball-reference.com/boxscores/202312220GSW.html', 'https://www.basketball-reference.com/boxscores/202312220SAC.html', 'https://www.basketball-reference.com/boxscores/202312230NYK.html', 'https://www.basketball-reference.com/boxscores/202312230LAC.html', 'https://www.basketball-reference.com/boxscores/202312230CHO.html', 'https://www.basketball-reference.com/boxscores/202312230IND.html', 'https://www.basketball-reference.com/boxscores/202312230NOP.html', 'https://www.basketball-reference.com/boxscores/202312230ATL.html', 'https://www.basketball-reference.com/boxscores/202312230BRK.html', 'https://www.basketball-reference.com/boxscores/202312230TOR.html', 'https://www.basketball-reference.com/boxscores/202312230CHI.html', 'https://www.basketball-reference.com/boxscores/202312230OKC.html', 'https://www.basketball-reference.com/boxscores/202312230DAL.html', 'https://www.basketball-reference.com/boxscores/202312230GSW.html', 'https://www.basketball-reference.com/boxscores/202312230SAC.html', 'https://www.basketball-reference.com/boxscores/202312250NYK.html', 'https://www.basketball-reference.com/boxscores/202312250DEN.html', 'https://www.basketball-reference.com/boxscores/202312250LAL.html', 'https://www.basketball-reference.com/boxscores/202312250MIA.html', 'https://www.basketball-reference.com/boxscores/202312250PHO.html', 'https://www.basketball-reference.com/boxscores/202312260DET.html', 'https://www.basketball-reference.com/boxscores/202312260WAS.html', 'https://www.basketball-reference.com/boxscores/202312260CHI.html', 'https://www.basketball-reference.com/boxscores/202312260HOU.html', 'https://www.basketball-reference.com/boxscores/202312260NOP.html', 'https://www.basketball-reference.com/boxscores/202312260OKC.html', 'https://www.basketball-reference.com/boxscores/202312260SAS.html', 'https://www.basketball-reference.com/boxscores/202312260POR.html', 'https://www.basketball-reference.com/boxscores/202312260LAC.html', 'https://www.basketball-reference.com/boxscores/202312270ORL.html', 'https://www.basketball-reference.com/boxscores/202312270WAS.html', 'https://www.basketball-reference.com/boxscores/202312270BRK.html', 'https://www.basketball-reference.com/boxscores/202312270HOU.html', 'https://www.basketball-reference.com/boxscores/202312270OKC.html', 'https://www.basketball-reference.com/boxscores/202312270DAL.html', 'https://www.basketball-reference.com/boxscores/202312280BOS.html', 'https://www.basketball-reference.com/boxscores/202312280CHI.html', 'https://www.basketball-reference.com/boxscores/202312280MIN.html', 'https://www.basketball-reference.com/boxscores/202312280NOP.html', 'https://www.basketball-reference.com/boxscores/202312280DEN.html', 'https://www.basketball-reference.com/boxscores/202312280GSW.html', 'https://www.basketball-reference.com/boxscores/202312280POR.html', 'https://www.basketball-reference.com/boxscores/202312280LAL.html', 'https://www.basketball-reference.com/boxscores/202312290ORL.html', 'https://www.basketball-reference.com/boxscores/202312290WAS.html', 'https://www.basketball-reference.com/boxscores/202312290ATL.html', 'https://www.basketball-reference.com/boxscores/202312290BOS.html', 'https://www.basketball-reference.com/boxscores/202312290CLE.html', 'https://www.basketball-reference.com/boxscores/202312290HOU.html', 'https://www.basketball-reference.com/boxscores/202312290DEN.html', 'https://www.basketball-reference.com/boxscores/202312290PHO.html', 'https://www.basketball-reference.com/boxscores/202312290POR.html', 'https://www.basketball-reference.com/boxscores/202312290LAC.html', 'https://www.basketball-reference.com/boxscores/202312300UTA.html', 'https://www.basketball-reference.com/boxscores/202312300DET.html', 'https://www.basketball-reference.com/boxscores/202312300IND.html', 'https://www.basketball-reference.com/boxscores/202312300CHI.html', 'https://www.basketball-reference.com/boxscores/202312300MIN.html', 'https://www.basketball-reference.com/boxscores/202312300GSW.html', 'https://www.basketball-reference.com/boxscores/202312310WAS.html', 'https://www.basketball-reference.com/boxscores/202312310NOP.html', 'https://www.basketball-reference.com/boxscores/202312310OKC.html', 'https://www.basketball-reference.com/boxscores/202312310SAS.html', 'https://www.basketball-reference.com/boxscores/202312310MEM.html', 'https://www.basketball-reference.com/boxscores/202312310PHO.html', 'https://www.basketball-reference.com/boxscores/202401010NYK.html', 'https://www.basketball-reference.com/boxscores/202401010TOR.html', 'https://www.basketball-reference.com/boxscores/202401010HOU.html', 'https://www.basketball-reference.com/boxscores/202401010MIL.html', 'https://www.basketball-reference.com/boxscores/202401010DEN.html', 'https://www.basketball-reference.com/boxscores/202401010PHO.html', 'https://www.basketball-reference.com/boxscores/202401010UTA.html', 'https://www.basketball-reference.com/boxscores/202401010LAC.html', 'https://www.basketball-reference.com/boxscores/202401020PHI.html', 'https://www.basketball-reference.com/boxscores/202401020MEM.html', 'https://www.basketball-reference.com/boxscores/202401020NOP.html', 'https://www.basketball-reference.com/boxscores/202401020OKC.html', 'https://www.basketball-reference.com/boxscores/202401020GSW.html', 'https://www.basketball-reference.com/boxscores/202401020SAC.html', 'https://www.basketball-reference.com/boxscores/202401030CLE.html', 'https://www.basketball-reference.com/boxscores/202401030IND.html', 'https://www.basketball-reference.com/boxscores/202401030ATL.html', 'https://www.basketball-reference.com/boxscores/202401030HOU.html', 'https://www.basketball-reference.com/boxscores/202401030MEM.html', 'https://www.basketball-reference.com/boxscores/202401030MIN.html', 'https://www.basketball-reference.com/boxscores/202401030DAL.html', 'https://www.basketball-reference.com/boxscores/202401030NYK.html', 'https://www.basketball-reference.com/boxscores/202401030PHO.html', 'https://www.basketball-reference.com/boxscores/202401030UTA.html', 'https://www.basketball-reference.com/boxscores/202401030LAL.html', 'https://www.basketball-reference.com/boxscores/202401030SAC.html', 'https://www.basketball-reference.com/boxscores/202401040SAS.html', 'https://www.basketball-reference.com/boxscores/202401040GSW.html', 'https://www.basketball-reference.com/boxscores/202401050BOS.html', 'https://www.basketball-reference.com/boxscores/202401050IND.html', 'https://www.basketball-reference.com/boxscores/202401050BRK.html', 'https://www.basketball-reference.com/boxscores/202401050CLE.html', 'https://www.basketball-reference.com/boxscores/202401050PHI.html', 'https://www.basketball-reference.com/boxscores/202401050CHI.html', 'https://www.basketball-reference.com/boxscores/202401050HOU.html', 'https://www.basketball-reference.com/boxscores/202401050NOP.html', 'https://www.basketball-reference.com/boxscores/202401050DAL.html', 'https://www.basketball-reference.com/boxscores/202401050DEN.html', 'https://www.basketball-reference.com/boxscores/202401050PHO.html', 'https://www.basketball-reference.com/boxscores/202401050GSW.html', 'https://www.basketball-reference.com/boxscores/202401050LAL.html', 'https://www.basketball-reference.com/boxscores/202401050SAC.html', 'https://www.basketball-reference.com/boxscores/202401060IND.html', 'https://www.basketball-reference.com/boxscores/202401060WAS.html', 'https://www.basketball-reference.com/boxscores/202401060PHI.html', 'https://www.basketball-reference.com/boxscores/202401060HOU.html', 'https://www.basketball-reference.com/boxscores/202401070CLE.html', 'https://www.basketball-reference.com/boxscores/202401070BRK.html', 'https://www.basketball-reference.com/boxscores/202401070ORL.html', 'https://www.basketball-reference.com/boxscores/202401070SAC.html', 'https://www.basketball-reference.com/boxscores/202401070DAL.html', 'https://www.basketball-reference.com/boxscores/202401070DEN.html', 'https://www.basketball-reference.com/boxscores/202401070PHO.html', 'https://www.basketball-reference.com/boxscores/202401070GSW.html', 'https://www.basketball-reference.com/boxscores/202401070LAL.html', 'https://www.basketball-reference.com/boxscores/202401080CHO.html', 'https://www.basketball-reference.com/boxscores/202401080IND.html', 'https://www.basketball-reference.com/boxscores/202401080WAS.html', 'https://www.basketball-reference.com/boxscores/202401080MIA.html', 'https://www.basketball-reference.com/boxscores/202401080MIL.html', 'https://www.basketball-reference.com/boxscores/202401080LAC.html', 'https://www.basketball-reference.com/boxscores/202401090DET.html', 'https://www.basketball-reference.com/boxscores/202401090ORL.html', 'https://www.basketball-reference.com/boxscores/202401090NYK.html', 'https://www.basketball-reference.com/boxscores/202401090DAL.html', 'https://www.basketball-reference.com/boxscores/202401090LAL.html', 'https://www.basketball-reference.com/boxscores/202401100BOS.html', 'https://www.basketball-reference.com/boxscores/202401100CHO.html', 'https://www.basketball-reference.com/boxscores/202401100DET.html', 'https://www.basketball-reference.com/boxscores/202401100IND.html', 'https://www.basketball-reference.com/boxscores/202401100ATL.html', 'https://www.basketball-reference.com/boxscores/202401100MIA.html', 'https://www.basketball-reference.com/boxscores/202401100CHI.html', 'https://www.basketball-reference.com/boxscores/202401100GSW.html', 'https://www.basketball-reference.com/boxscores/202401100UTA.html', 'https://www.basketball-reference.com/boxscores/202401100LAC.html', 'https://www.basketball-reference.com/boxscores/202401110CLE.html', 'https://www.basketball-reference.com/boxscores/202401110MIL.html', 'https://www.basketball-reference.com/boxscores/202401110OKC.html', 'https://www.basketball-reference.com/boxscores/202401110DAL.html', 'https://www.basketball-reference.com/boxscores/202401110LAL.html', 'https://www.basketball-reference.com/boxscores/202401120ATL.html', 'https://www.basketball-reference.com/boxscores/202401120DET.html', 'https://www.basketball-reference.com/boxscores/202401120PHI.html', 'https://www.basketball-reference.com/boxscores/202401120CHI.html', 'https://www.basketball-reference.com/boxscores/202401120MEM.html', 'https://www.basketball-reference.com/boxscores/202401120MIA.html', 'https://www.basketball-reference.com/boxscores/202401120MIN.html', 'https://www.basketball-reference.com/boxscores/202401120SAS.html', 'https://www.basketball-reference.com/boxscores/202401120UTA.html', 'https://www.basketball-reference.com/boxscores/202401120DEN.html', 'https://www.basketball-reference.com/boxscores/202401130BOS.html', 'https://www.basketball-reference.com/boxscores/202401130ATL.html', 'https://www.basketball-reference.com/boxscores/202401130MEM.html', 'https://www.basketball-reference.com/boxscores/202401130MIL.html', 'https://www.basketball-reference.com/boxscores/202401130OKC.html', 'https://www.basketball-reference.com/boxscores/202401130DAL.html', 'https://www.basketball-reference.com/boxscores/202401130SAS.html', 'https://www.basketball-reference.com/boxscores/202401130UTA.html', 'https://www.basketball-reference.com/boxscores/202401140DEN.html', 'https://www.basketball-reference.com/boxscores/202401140MIA.html', 'https://www.basketball-reference.com/boxscores/202401140MIL.html', 'https://www.basketball-reference.com/boxscores/202401140MIN.html', 'https://www.basketball-reference.com/boxscores/202401140POR.html', 'https://www.basketball-reference.com/boxscores/202401150PHI.html', 'https://www.basketball-reference.com/boxscores/202401150DAL.html', 'https://www.basketball-reference.com/boxscores/202401150NYK.html', 'https://www.basketball-reference.com/boxscores/202401150WAS.html', 'https://www.basketball-reference.com/boxscores/202401150ATL.html', 'https://www.basketball-reference.com/boxscores/202401150MEM.html', 'https://www.basketball-reference.com/boxscores/202401150CLE.html', 'https://www.basketball-reference.com/boxscores/202401150BRK.html', 'https://www.basketball-reference.com/boxscores/202401150TOR.html', 'https://www.basketball-reference.com/boxscores/202401150UTA.html', 'https://www.basketball-reference.com/boxscores/202401150LAL.html', 'https://www.basketball-reference.com/boxscores/202401160PHI.html', 'https://www.basketball-reference.com/boxscores/202401160PHO.html', 'https://www.basketball-reference.com/boxscores/202401160LAC.html', 'https://www.basketball-reference.com/boxscores/202401170DET.html', 'https://www.basketball-reference.com/boxscores/202401170ATL.html', 'https://www.basketball-reference.com/boxscores/202401170BOS.html', 'https://www.basketball-reference.com/boxscores/202401170CLE.html', 'https://www.basketball-reference.com/boxscores/202401170NYK.html', 'https://www.basketball-reference.com/boxscores/202401170TOR.html', 'https://www.basketball-reference.com/boxscores/202401170NOP.html', 'https://www.basketball-reference.com/boxscores/202401170LAL.html', 'https://www.basketball-reference.com/boxscores/202401170POR.html', 'https://www.basketball-reference.com/boxscores/202401180NYK.html', 'https://www.basketball-reference.com/boxscores/202401180TOR.html', 'https://www.basketball-reference.com/boxscores/202401180UTA.html', 'https://www.basketball-reference.com/boxscores/202401180MIN.html', 'https://www.basketball-reference.com/boxscores/202401180SAC.html', 'https://www.basketball-reference.com/boxscores/202401190CHO.html', 'https://www.basketball-reference.com/boxscores/202401190ORL.html', 'https://www.basketball-reference.com/boxscores/202401190BOS.html', 'https://www.basketball-reference.com/boxscores/202401190MIA.html', 'https://www.basketball-reference.com/boxscores/202401190NOP.html', 'https://www.basketball-reference.com/boxscores/202401190POR.html', 'https://www.basketball-reference.com/boxscores/202401190LAL.html', 'https://www.basketball-reference.com/boxscores/202401200DET.html', 'https://www.basketball-reference.com/boxscores/202401200CHO.html', 'https://www.basketball-reference.com/boxscores/202401200WAS.html', 'https://www.basketball-reference.com/boxscores/202401200ATL.html', 'https://www.basketball-reference.com/boxscores/202401200NYK.html', 'https://www.basketball-reference.com/boxscores/202401200CHI.html', 'https://www.basketball-reference.com/boxscores/202401200HOU.html', 'https://www.basketball-reference.com/boxscores/202401200MIN.html', 'https://www.basketball-reference.com/boxscores/202401210LAC.html', 'https://www.basketball-reference.com/boxscores/202401210ORL.html', 'https://www.basketball-reference.com/boxscores/202401210WAS.html', 'https://www.basketball-reference.com/boxscores/202401210HOU.html', 'https://www.basketball-reference.com/boxscores/202401210PHO.html', 'https://www.basketball-reference.com/boxscores/202401210LAL.html', 'https://www.basketball-reference.com/boxscores/202401220DET.html', 'https://www.basketball-reference.com/boxscores/202401220ORL.html', 'https://www.basketball-reference.com/boxscores/202401220PHI.html', 'https://www.basketball-reference.com/boxscores/202401220TOR.html', 'https://www.basketball-reference.com/boxscores/202401220MIN.html', 'https://www.basketball-reference.com/boxscores/202401220DAL.html', 'https://www.basketball-reference.com/boxscores/202401220PHO.html', 'https://www.basketball-reference.com/boxscores/202401220SAC.html', 'https://www.basketball-reference.com/boxscores/202401230IND.html', 'https://www.basketball-reference.com/boxscores/202401230BRK.html', 'https://www.basketball-reference.com/boxscores/202401230NOP.html', 'https://www.basketball-reference.com/boxscores/202401230OKC.html', 'https://www.basketball-reference.com/boxscores/202401230LAC.html', 'https://www.basketball-reference.com/boxscores/202401240DET.html', 'https://www.basketball-reference.com/boxscores/202401240WAS.html', 'https://www.basketball-reference.com/boxscores/202401240MIA.html', 'https://www.basketball-reference.com/boxscores/202401240HOU.html', 'https://www.basketball-reference.com/boxscores/202401240MIL.html', 'https://www.basketball-reference.com/boxscores/202401240DAL.html', 'https://www.basketball-reference.com/boxscores/202401240SAS.html', 'https://www.basketball-reference.com/boxscores/202401240GSW.html', 'https://www.basketball-reference.com/boxscores/202401250IND.html', 'https://www.basketball-reference.com/boxscores/202401250WAS.html', 'https://www.basketball-reference.com/boxscores/202401250BRK.html', 'https://www.basketball-reference.com/boxscores/202401250MIA.html', 'https://www.basketball-reference.com/boxscores/202401250NYK.html', 'https://www.basketball-reference.com/boxscores/202401250GSW.html', 'https://www.basketball-reference.com/boxscores/202401250LAL.html', 'https://www.basketball-reference.com/boxscores/202401260ATL.html', 'https://www.basketball-reference.com/boxscores/202401260CHO.html', 'https://www.basketball-reference.com/boxscores/202401260IND.html', 'https://www.basketball-reference.com/boxscores/202401260TOR.html', 'https://www.basketball-reference.com/boxscores/202401260MEM.html', 'https://www.basketball-reference.com/boxscores/202401260MIL.html', 'https://www.basketball-reference.com/boxscores/202401260NOP.html', 'https://www.basketball-reference.com/boxscores/202401260SAS.html', 'https://www.basketball-reference.com/boxscores/202401270DET.html', 'https://www.basketball-reference.com/boxscores/202401270NYK.html', 'https://www.basketball-reference.com/boxscores/202401270DEN.html', 'https://www.basketball-reference.com/boxscores/202401270BRK.html', 'https://www.basketball-reference.com/boxscores/202401270BOS.html', 'https://www.basketball-reference.com/boxscores/202401270CHO.html', 'https://www.basketball-reference.com/boxscores/202401270MIL.html', 'https://www.basketball-reference.com/boxscores/202401270GSW.html', 'https://www.basketball-reference.com/boxscores/202401270SAS.html', 'https://www.basketball-reference.com/boxscores/202401270DAL.html', 'https://www.basketball-reference.com/boxscores/202401280DET.html', 'https://www.basketball-reference.com/boxscores/202401280IND.html', 'https://www.basketball-reference.com/boxscores/202401280ATL.html', 'https://www.basketball-reference.com/boxscores/202401280ORL.html', 'https://www.basketball-reference.com/boxscores/202401280POR.html', 'https://www.basketball-reference.com/boxscores/202401290CHO.html', 'https://www.basketball-reference.com/boxscores/202401290CLE.html', 'https://www.basketball-reference.com/boxscores/202401290BOS.html', 'https://www.basketball-reference.com/boxscores/202401290BRK.html', 'https://www.basketball-reference.com/boxscores/202401290MIA.html', 'https://www.basketball-reference.com/boxscores/202401290HOU.html', 'https://www.basketball-reference.com/boxscores/202401290MEM.html', 'https://www.basketball-reference.com/boxscores/202401290OKC.html', 'https://www.basketball-reference.com/boxscores/202401290SAS.html', 'https://www.basketball-reference.com/boxscores/202401290DAL.html', 'https://www.basketball-reference.com/boxscores/202401290DEN.html', 'https://www.basketball-reference.com/boxscores/202401290POR.html', 'https://www.basketball-reference.com/boxscores/202401300ATL.html', 'https://www.basketball-reference.com/boxscores/202401300BOS.html', 'https://www.basketball-reference.com/boxscores/202401300NYK.html', 'https://www.basketball-reference.com/boxscores/202401300CHI.html', 'https://www.basketball-reference.com/boxscores/202401300GSW.html', 'https://www.basketball-reference.com/boxscores/202401310CHO.html', 'https://www.basketball-reference.com/boxscores/202401310CLE.html', 'https://www.basketball-reference.com/boxscores/202401310WAS.html', 'https://www.basketball-reference.com/boxscores/202401310MIA.html', 'https://www.basketball-reference.com/boxscores/202401310HOU.html', 'https://www.basketball-reference.com/boxscores/202401310MIN.html', 'https://www.basketball-reference.com/boxscores/202401310OKC.html', 'https://www.basketball-reference.com/boxscores/202401310SAS.html', 'https://www.basketball-reference.com/boxscores/202401310BRK.html', 'https://www.basketball-reference.com/boxscores/202401310POR.html', 'https://www.basketball-reference.com/boxscores/202402010BOS.html', 'https://www.basketball-reference.com/boxscores/202402010NYK.html', 'https://www.basketball-reference.com/boxscores/202402010MEM.html', 'https://www.basketball-reference.com/boxscores/202402010UTA.html', 'https://www.basketball-reference.com/boxscores/202402020DET.html', 'https://www.basketball-reference.com/boxscores/202402020WAS.html', 'https://www.basketball-reference.com/boxscores/202402020ATL.html', 'https://www.basketball-reference.com/boxscores/202402020IND.html', 'https://www.basketball-reference.com/boxscores/202402020HOU.html', 'https://www.basketball-reference.com/boxscores/202402020MEM.html', 'https://www.basketball-reference.com/boxscores/202402020MIN.html', 'https://www.basketball-reference.com/boxscores/202402020OKC.html', 'https://www.basketball-reference.com/boxscores/202402020SAS.html', 'https://www.basketball-reference.com/boxscores/202402020DEN.html', 'https://www.basketball-reference.com/boxscores/202402030PHI.html', 'https://www.basketball-reference.com/boxscores/202402030ATL.html', 'https://www.basketball-reference.com/boxscores/202402030CHI.html', 'https://www.basketball-reference.com/boxscores/202402030DAL.html', 'https://www.basketball-reference.com/boxscores/202402030NYK.html', 'https://www.basketball-reference.com/boxscores/202402030SAS.html', 'https://www.basketball-reference.com/boxscores/202402040DET.html', 'https://www.basketball-reference.com/boxscores/202402040WAS.html', 'https://www.basketball-reference.com/boxscores/202402040BOS.html', 'https://www.basketball-reference.com/boxscores/202402040CHO.html', 'https://www.basketball-reference.com/boxscores/202402040MIA.html', 'https://www.basketball-reference.com/boxscores/202402040MIN.html', 'https://www.basketball-reference.com/boxscores/202402040OKC.html', 'https://www.basketball-reference.com/boxscores/202402040UTA.html', 'https://www.basketball-reference.com/boxscores/202402040DEN.html', 'https://www.basketball-reference.com/boxscores/202402050CHO.html', 'https://www.basketball-reference.com/boxscores/202402050CLE.html', 'https://www.basketball-reference.com/boxscores/202402050PHI.html', 'https://www.basketball-reference.com/boxscores/202402050ATL.html', 'https://www.basketball-reference.com/boxscores/202402050BRK.html', 'https://www.basketball-reference.com/boxscores/202402050NOP.html', 'https://www.basketball-reference.com/boxscores/202402060IND.html', 'https://www.basketball-reference.com/boxscores/202402060BRK.html', 'https://www.basketball-reference.com/boxscores/202402060MIA.html', 'https://www.basketball-reference.com/boxscores/202402060NYK.html', 'https://www.basketball-reference.com/boxscores/202402060CHI.html', 'https://www.basketball-reference.com/boxscores/202402060UTA.html', 'https://www.basketball-reference.com/boxscores/202402060PHO.html', 'https://www.basketball-reference.com/boxscores/202402070CHO.html', 'https://www.basketball-reference.com/boxscores/202402070WAS.html', 'https://www.basketball-reference.com/boxscores/202402070BOS.html', 'https://www.basketball-reference.com/boxscores/202402070MIA.html', 'https://www.basketball-reference.com/boxscores/202402070PHI.html', 'https://www.basketball-reference.com/boxscores/202402070LAC.html', 'https://www.basketball-reference.com/boxscores/202402070SAC.html', 'https://www.basketball-reference.com/boxscores/202402080IND.html', 'https://www.basketball-reference.com/boxscores/202402080ORL.html', 'https://www.basketball-reference.com/boxscores/202402080BRK.html', 'https://www.basketball-reference.com/boxscores/202402080NYK.html', 'https://www.basketball-reference.com/boxscores/202402080MEM.html', 'https://www.basketball-reference.com/boxscores/202402080MIL.html', 'https://www.basketball-reference.com/boxscores/202402080PHO.html', 'https://www.basketball-reference.com/boxscores/202402080LAL.html', 'https://www.basketball-reference.com/boxscores/202402080POR.html']

    pages = list(get_html_pages(links))
    print('writing pages to csv**********************************************')
    [tables_to_csv(page) for page in pages]
    # map(tables_to_csv, pages)

if __name__ == '__main__':
    write_all_box_score_pages_to_csv()
