import re
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup



team_links = [("https://www.basketball-reference.com/teams/ATL/2024.html", 'ATL'),
             ("https://www.basketball-reference.com/teams/BOS/2024.html", 'BOS'),
             ("https://www.basketball-reference.com/teams/PHI/2024.html", 'PHI'),
             ("https://www.basketball-reference.com/teams/BRK/2024.html", 'BRK'),
             ("https://www.basketball-reference.com/teams/TOR/2024.html", 'TOR'),
             ("https://www.basketball-reference.com/teams/CLE/2024.html", 'CLE'),
             ("https://www.basketball-reference.com/teams/MIL/2024.html", 'MIL'),
             ("https://www.basketball-reference.com/teams/IND/2024.html", 'IND'),
             ("https://www.basketball-reference.com/teams/CHI/2024.html", 'CHI'),
             ("https://www.basketball-reference.com/teams/DET/2024.html", 'DET'),
             ("https://www.basketball-reference.com/teams/ORL/2024.html", 'ORL'),
             ("https://www.basketball-reference.com/teams/MIA/2024.html", 'MIA'),
             ("https://www.basketball-reference.com/teams/CHO/2024.html", 'CHO'),
             ("https://www.basketball-reference.com/teams/WAS/2024.html", 'WAS'),
             ("https://www.basketball-reference.com/teams/MIN/2024.html", 'MIN'),
             ("https://www.basketball-reference.com/teams/OKC/2024.html", 'OKC'),
             ("https://www.basketball-reference.com/teams/DEN/2024.html", 'DEN'),
             ("https://www.basketball-reference.com/teams/UTA/2024.html", 'UTA'),
             ("https://www.basketball-reference.com/teams/POR/2024.html", 'POR'),
             ("https://www.basketball-reference.com/teams/LAC/2024.html", 'LAC'),
             ("https://www.basketball-reference.com/teams/SAC/2024.html", 'SAC'),
             ("https://www.basketball-reference.com/teams/PHO/2024.html", 'PHO'),
             ("https://www.basketball-reference.com/teams/LAL/2024.html", 'LAL'),
             ("https://www.basketball-reference.com/teams/GSW/2024.html", 'GSW'),
             ("https://www.basketball-reference.com/teams/NOP/2024.html", 'NOP'),
             ("https://www.basketball-reference.com/teams/DAL/2024.html", 'DAL'),
             ("https://www.basketball-reference.com/teams/HOU/2024.html", 'HOU'),
             ("https://www.basketball-reference.com/teams/MEM/2024.html", 'MEM'),
             ("https://www.basketball-reference.com/teams/SAS/2024.html", 'SAS'),
             ("https://www.basketball-reference.com/teams/NYK/2024.html", 'NYK')]



def extract_team_name_from_link(link):
    pattern = r'/teams/([A-Z]+)/'
    match = re.search(pattern, link)
    if match:
        team_name = match.group(1)
        return team_name
    else:
        return None


def get_web_element_by_id(link, element_id, driver):
    driver.get(link)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, element_id))
    )
    return driver.find_element(By.ID, element_id)







def get_html_from_web_element(web_element):
    return web_element.get_attribute('outerHTML')


def get_html_table_data(html_table):
    data = []
    for row in html_table.find_all('tr'):
        cols = row.find_all(['th', 'td'])
        cols = [col.text.strip() for col in cols]
        # Exclude rows with 'Did Not Play' status
        if 'Did Not Play' not in cols:
            data.append(cols)
    return data



def create_database_table(conn,schema):
    c = conn.cursor()
    c.execute(schema)


def insert_data_into_per_100_possesions_table(conn, data):
    c = conn.cursor()
    print(data)
    for row in data[1:]:
        if len(row) == 30:
            c.execute('''INSERT INTO per_100_possesion VALUES (
?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
?, ?, ?, ?, ?, ?,?,?,?)''', row)


def insert_data_into_per_36(conn, data):
    c = conn.cursor()
    for row in data[1:]:
        if len(row) == 27:
            c.execute('''INSERT INTO per_36 VALUES (
?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', row)


def insert_data_into_per_game_table(conn, data):
        c = conn.cursor()
        for row in data[1:]:
            if len(row) == 28:
                c.execute(
                    '''INSERT INTO per_game VALUES (
?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',row)


def insert_data_into_team_and_opponent_table(conn, data):
    c = conn.cursor()
    for row in data[1:]:
        if len(row) == 24:
            c.execute('''INSERT INTO team_and_opponent VALUES (
?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
 ?, ?, ?)''', row)


def insert_data_into_roster__table(conn, data):
    c = conn.cursor()
    for row in data[1:]:
        if len(row) == 9:
            c.execute('''INSERT INTO roster VALUES (
?, ?, ?, ?, ?, ?, ?, ?, ?)''', row)


def insert_data_into_advanced_table(conn, data):
    c = conn.cursor()
    for row in data[1:]:
        if len(row) == 27:
            c.execute('''INSERT INTO advanced VALUES (
?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
?, ?, ?, ?, ?, ?, ?, ?, ?)''', row)


def insert_data_into_info_table(conn, data):
    c = conn.cursor()
    for row in data[2:]:
        if len(row) == 23:
            c.execute('''INSERT INTO team_info VALUES (
?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
 ?, ?, ?, ?)''',row)


def insert_data_into_adjusted_shooting_table(conn, data):
    c = conn.cursor()
    for row in data[2:]:
        if len(row) == 26:
            c.execute('''INSERT INTO adjusted_shooting VALUES (
?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
?, ?, ?, ?,?,?,?)''',
                row)


def insert_data_into_shooting_table(conn, data):
    c = conn.cursor()
    for row in data[2:]:
        if len(row) == 33:
            c.execute('''INSERT INTO shooting VALUES ( 
?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',row)


def insert_data_into_play_by_play_table(conn, data):
    c = conn.cursor()
    for row in data[2:]:
        if len(row) == 21:
            c.execute( '''INSERT INTO play_by_play VALUES (
?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',row)


def get_table_by_id(link, id ,driver):
    html_table = get_html_from_web_element(get_web_element_by_id(link, id, driver))
    return BeautifulSoup(html_table, 'html.parser')


def get_data(table):
    return get_html_table_data(table)


def get_bs4_tables_by_specific_ids(link, driver=webdriver.Firefox()):
    driver.get(link)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, 'content'))
    )
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    content_div = soup.find('div', id='content')
    tables = content_div.find_all('table')
    table_ids = ['roster',
                 'team_and_opponent',
                 'team_misc',
                 'per_game',
                 'totals',
                 'per_minute',
                 'per_poss',
                 'adj_shooting',
                 'shooting',
                 'pbp', 'advanced']
    # Filter tables based on provided IDs and create tuple
    selected_tables = [(table.get('id'), table) for table in tables if table.get('id') in table_ids]
    driver.close()

    return selected_tables

def insert_data(link,team_name):
    tables = get_bs4_tables_by_specific_ids(link)
    for table_id, table in tables:
        data = get_data(table)
        # print(data)
        print(table_id)
        # print(table)
        try:
            # Connect to the database
            conn = sqlite3.connect(f'nba_databases/{team_name}.db')
            # Insert data into the roster table
            # if table_id == 'pbp':
            #     insert_data_into_play_by_play_table(conn, data)
            #     conn.commit()
            #     print("Inserted play by play data successfully!")
            # if table_id == 'roster':
            #     insert_data_into_roster__table(conn, data)
            #     conn.commit()
            #     print("Inserted roster data successfully!")
            # if table_id == 'team_and_opponent':
            #     insert_data_into_team_and_opponent_table(conn, data)
            #     conn.commit()
            #     print("Inserted team and opponent data successfully!")
            # if table_id == 'team_misc':
            #     insert_data_into_info_table(conn, data)
            #     conn.commit()
            #     print("Inserted team info data successfully!")
            # if table_id == 'per_game':
            #     insert_data_into_per_game_table(conn, data)
            #     conn.commit()
            #     print("Inserted per game data successfully!")
            # if table_id == 'per_minute':
            #     insert_data_into_per_36(conn, data)
            #     conn.commit()
            #     print("Inserted per 36 minutes data successfully!")
            if table_id == 'per_poss':
                insert_data_into_per_100_possesions_table(conn, data)
                conn.commit()
                print("Inserted per 100 possesions successfully!")
            # if table_id == 'adj_shooting':
            #     insert_data_into_adjusted_shooting_table(conn, data)
            #     conn.commit()
            #     print("Inserted adjusted shooting data successfully!")
            # if table_id == 'advanced':
            #     insert_data_into_advanced_table(conn, data)
            #     conn.commit()
            #     print("Inserted advanced data successfully!")
            # if table_id == 'shooting':
            #     insert_data_into_shooting_table(conn, data)
            #     conn.commit()
            #     print("Inserted shooting data successfully!")

            else:print(f'Error while processing {table_id}')

        except Exception as e:
            print("An error occurred:", str(e))
        finally:
            # Close the database connection
            conn.close()


insert_data('https://www.basketball-reference.com/teams/ATL/2024.html', 'ATL')

# driver = webdriver.Firefox()
# table_ids = ['roster',
# 'team_and_opponent',
# 'team_misc',
# 'per_game',
# 'totals',
# 'per_minute',
# 'per_poss',
# 'adj_shooting',
# 'shooting',
# 'pbp','advanced']
# tabless = get_bs4_tables_by_specific_ids("https://www.basketball-reference.com/teams/BOS/2024.html", driver, table_ids)
# driver.close()
# print(len(tabless))
# print(tabless[0])
# # print(tables[1])
# # print(tables[2])
# # print(tables[3])
# print(tables[4])
# print(tables[5])
# print(tables[6])
# print(tables[7])
# print(tables[8])
# print(tables[9])
# print(tables[10])

# [insert_data(link, team_name) for link, team_name in team_links]
