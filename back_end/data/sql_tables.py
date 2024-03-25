from bs4 import BeautifulSoup
import requests
import time
import sqlite3
import re
from teams_enum import NBATeam
from datetime import datetime

advanced_schema = '''CREATE TABLE IF NOT EXISTS advanced_game (
box_score_id TEXT, player_name TEXT, minutes TEXT, true_shooting_pct TEXT, effective_FG_pct TEXT,
 _3P_attempts_rate TEXT, FT_rate TEXT, ORB_pct TEXT, DRB_pct TEXT, TRB_pct TEXT,
  AST_pct TEXT, STL_pct TEXT, BLK_pct TEXT, TOV_pct TEXT, USG_pct TEXT, ORtg TEXT,
   DRtg TEXT, BPM TEXT, HOME TEXT, AWAY TEXT, game_date TEXT)'''

advanced_insert_schema = 'INSERT INTO advanced_game VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'

basic_game_schema = '''CREATE TABLE IF NOT EXISTS basic_game
                    (box_score_id TEXT, Player TEXT, MP TEXT, FG TEXT, FGA TEXT, FG_PCT TEXT, 
                    FG3 TEXT, FG3A TEXT, FG3_PCT TEXT, FT TEXT, FTA TEXT, 
                    FT_PCT TEXT, ORB TEXT, DRB TEXT, TRB TEXT, AST TEXT, 
                    STL TEXT, BLK TEXT, TOV TEXT, PF TEXT, PTS TEXT, 
                    PLUS_MINUS TEXT, HOME TEXT, AWAY TEXT, game_date TEXT)'''


insert_game_schema = 'INSERT INTO basic_game  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'

basic_q1_schema = '''CREATE TABLE IF NOT EXISTS basic_q1
                    (box_score_id TEXT, Player TEXT, MP TEXT, FG TEXT, FGA TEXT, FG_PCT TEXT, 
                    FG3 TEXT, FG3A TEXT, FG3_PCT TEXT, FT TEXT, FTA TEXT, 
                    FT_PCT TEXT, ORB TEXT, DRB TEXT, TRB TEXT, AST TEXT, 
                    STL TEXT, BLK TEXT, TOV TEXT, PF TEXT, PTS TEXT, 
                    PLUS_MINUS TEXT, HOME TEXT, AWAY TEXT, game_date TEXT)'''

insert_q1_schema = 'INSERT INTO basic_q1  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'

basic_q2_schema = '''CREATE TABLE IF NOT EXISTS basic_q2
                    (box_score_id TEXT, Player TEXT, MP TEXT, FG TEXT, FGA TEXT, FG_PCT TEXT, 
                    FG3 TEXT, FG3A TEXT, FG3_PCT TEXT, FT TEXT, FTA TEXT, 
                    FT_PCT TEXT, ORB TEXT, DRB TEXT, TRB TEXT, AST TEXT, 
                    STL TEXT, BLK TEXT, TOV TEXT, PF TEXT, PTS TEXT, 
                    PLUS_MINUS TEXT, HOME TEXT, AWAY TEXT, game_date TEXT)'''

insert_q2_schema = 'INSERT INTO basic_q2  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'

basic_h1_schema = '''CREATE TABLE IF NOT EXISTS basic_h1
                    (box_score_id TEXT, Player TEXT, MP TEXT, FG TEXT, FGA TEXT, FG_PCT TEXT, 
                    FG3 TEXT, FG3A TEXT, FG3_PCT TEXT, FT TEXT, FTA TEXT, 
                    FT_PCT TEXT, ORB TEXT, DRB TEXT, TRB TEXT, AST TEXT, 
                    STL TEXT, BLK TEXT, TOV TEXT, PF TEXT, PTS TEXT, 
                    PLUS_MINUS TEXT, HOME TEXT, AWAY TEXT, game_date TEXT)'''

insert_h1_schema = 'INSERT INTO basic_h1  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'


basic_q3_schema = '''CREATE TABLE IF NOT EXISTS basic_q3
                    (box_score_id TEXT, Player TEXT, MP TEXT, FG TEXT, FGA TEXT, FG_PCT TEXT, 
                    FG3 TEXT, FG3A TEXT, FG3_PCT TEXT, FT TEXT, FTA TEXT, 
                    FT_PCT TEXT, ORB TEXT, DRB TEXT, TRB TEXT, AST TEXT, 
                    STL TEXT, BLK TEXT, TOV TEXT, PF TEXT, PTS TEXT, 
                    PLUS_MINUS TEXT, HOME TEXT, AWAY TEXT, game_date TEXT)'''

insert_q3_schema = 'INSERT INTO basic_q3  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'

basic_q4_schema = '''CREATE TABLE IF NOT EXISTS basic_q4
                    (box_score_id TEXT, Player TEXT, MP TEXT, FG TEXT, FGA TEXT, FG_PCT TEXT, 
                    FG3 TEXT, FG3A TEXT, FG3_PCT TEXT, FT TEXT, FTA TEXT, 
                    FT_PCT TEXT, ORB TEXT, DRB TEXT, TRB TEXT, AST TEXT, 
                    STL TEXT, BLK TEXT, TOV TEXT, PF TEXT, PTS TEXT, 
                    PLUS_MINUS TEXT, HOME TEXT, AWAY TEXT, game_date TEXT)'''

insert_q4_schema = 'INSERT INTO basic_q4 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'

basic_h2_schema = '''CREATE TABLE IF NOT EXISTS basic_h2
                    (box_score_id TEXT, Player TEXT, MP TEXT, FG TEXT, FGA TEXT, FG_PCT TEXT, 
                    FG3 TEXT, FG3A TEXT, FG3_PCT TEXT, FT TEXT, FTA TEXT, 
                    FT_PCT TEXT, ORB TEXT, DRB TEXT, TRB TEXT, AST TEXT, 
                    STL TEXT, BLK TEXT, TOV TEXT, PF TEXT, PTS TEXT, 
                    PLUS_MINUS TEXT, HOME TEXT, AWAY TEXT, game_date TEXT)'''

insert_h2_schema = 'INSERT INTO basic_h2  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
basic_ot1_schema = '''CREATE TABLE IF NOT EXISTS basic_ot1
                    (box_score_id TEXT, Player TEXT, MP TEXT, FG TEXT, FGA TEXT, FG_PCT TEXT, 
                    FG3 TEXT, FG3A TEXT, FG3_PCT TEXT, FT TEXT, FTA TEXT, 
                    FT_PCT TEXT, ORB TEXT, DRB TEXT, TRB TEXT, AST TEXT, 
                    STL TEXT, BLK TEXT, TOV TEXT, PF TEXT, PTS TEXT, 
                    PLUS_MINUS TEXT, HOME TEXT, AWAY TEXT, game_date TEXT)'''

insert_ot1_schema = 'INSERT INTO basic_ot1  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'




def send_request_for_one_html_page_to_site(url):
    try:
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0'
        })
        response.raise_for_status()
        print("Thread going to sleep for 5 seconds request sent")
        time.sleep(5)
        return BeautifulSoup(response.content, 'html.parser')
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

def get_all_tables(page):
    tables = page.find_all('table')
    return tables

def html_table_to_sqlite(html_table,schema,insert,game_id,home,away,date):
    rows = html_table.find_all('tr')
    conn = sqlite3.connect('nba_databases/NBA.db')
    cursor = conn.cursor()
    cursor.execute(schema)
    for row in rows[2:]:
        # print(len(row))
        # print(row)
        cols = row.find_all(['th', 'td'])
        values = [col.get_text() for col in cols]
        values.insert(0, game_id)
        values.append(home)
        values.append(away)
        values.append(date)
        if len(values) == 25:  # ensure we have all columns filled
            cursor.execute(insert, values)
        if len(values) == 21:  # ensure we have all columns filled
            cursor.execute(insert, values)
    # Commit changes and close connection
    conn.commit()
    conn.close()


def get_game_details_joined_for_table(page):
    details = page.find(id='content').find('h1').get_text()
    return details.replace(' ', '').replace(',', '_')


def get_game_info(game_string):
    # Regular expression pattern to extract game details, team names, and date
    pattern = r'(?:In-SeasonTournamentFinal:)?([A-Z][a-z0-9]+(?:[A-Z][a-z0-9]+)*)at([A-Z][a-z0-9]+(?:[A-Z][a-z0-9]+)*)BoxScore_(\w+\d+_\d+)'
    # Extracting information from each string
    match = re.match(pattern, game_string)
    if match:
        team1 = match.group(1)
        team2 = match.group(2)
        date = match.group(3)
        # Insert spaces between camel case team names
        away = re.sub(r"(?<=\w)([A-Z])", r" \1", team1)
        home = re.sub(r"(?<=\w)([A-Z])", r" \1", team2)
        date_obj = datetime.strptime(date, '%B%d_%Y')
        nba = NBATeam
        formatted_date = date_obj.strftime('%Y-%m-%d')
        print("Game:", away, "@", home)
        return (nba.get_team_abbreviation(away), nba.get_team_abbreviation(home),
                formatted_date, f"{away} @ {home}")
    else:
        print("No match found for:", game_string)

def get_html_table_data(html_table):
    data = []
    for row in html_table.find_all('tr'):
        cols = row.find_all(['th', 'td'])
        cols = [col.text.strip() for col in cols]
        data.append(cols)
    # print(data)
    return data


def run_script(link):
    print(link)
    page = send_request_for_one_html_page_to_site(link)
    tables = get_all_tables(page)
    print(len(tables))
    # print(tables[16])
    info = get_game_info(get_game_details_joined_for_table(page))
    home, away, date, game_info = info
    game_id = f'{date}{away}@{home}'
    if len(tables) == 16:
        html_table_to_sqlite(tables[0], basic_game_schema, insert_game_schema, game_id, home, away, date)
        html_table_to_sqlite(tables[1], basic_q1_schema, insert_q1_schema, game_id, home, away, date)
        html_table_to_sqlite(tables[2], basic_q2_schema, insert_q2_schema, game_id, home, away, date)
        html_table_to_sqlite(tables[3], basic_h1_schema, insert_h1_schema, game_id, home, away, date)
        html_table_to_sqlite(tables[4], basic_q3_schema, insert_q3_schema, game_id, home, away, date)
        html_table_to_sqlite(tables[5], basic_q4_schema, insert_q4_schema, game_id, home, away, date)
        html_table_to_sqlite(tables[6], basic_h2_schema, insert_h2_schema, game_id, home, away, date)
        html_table_to_sqlite(tables[7], advanced_schema, advanced_insert_schema, game_id, home, away, date)
        html_table_to_sqlite(tables[8], basic_game_schema, insert_game_schema, game_id, home, away, date)
        html_table_to_sqlite(tables[9], basic_q1_schema, insert_q1_schema, game_id, home, away, date)
        html_table_to_sqlite(tables[10], basic_q2_schema, insert_q2_schema, game_id, home, away, date)
        html_table_to_sqlite(tables[11], basic_h1_schema, insert_h1_schema, game_id, home, away, date)
        html_table_to_sqlite(tables[12], basic_q3_schema, insert_q3_schema, game_id, home, away, date)
        html_table_to_sqlite(tables[13], basic_q4_schema, insert_q4_schema, game_id, home, away, date)
        html_table_to_sqlite(tables[14], basic_h2_schema, insert_h2_schema, game_id, home, away, date)
        html_table_to_sqlite(tables[15], advanced_schema, advanced_insert_schema, game_id, home, away, date)
    if len(tables) == 18:
        html_table_to_sqlite(tables[0], basic_game_schema, insert_game_schema, game_id, home, away, date)
        html_table_to_sqlite(tables[1], basic_q1_schema, insert_q1_schema, game_id, home, away, date)
        html_table_to_sqlite(tables[2], basic_q2_schema, insert_q2_schema, game_id, home, away, date)
        html_table_to_sqlite(tables[3], basic_h1_schema, insert_h1_schema, game_id, home, away, date)
        html_table_to_sqlite(tables[4], basic_q3_schema, insert_q3_schema, game_id, home, away, date)
        html_table_to_sqlite(tables[5], basic_q4_schema, insert_q4_schema, game_id, home, away, date)
        html_table_to_sqlite(tables[6], basic_h2_schema, insert_h2_schema, game_id, home, away, date)
        html_table_to_sqlite(tables[7], basic_ot1_schema, insert_ot1_schema, game_id, home, away, date)
        html_table_to_sqlite(tables[8], advanced_schema, advanced_insert_schema, game_id, home, away, date)
        html_table_to_sqlite(tables[9], basic_game_schema, insert_game_schema, game_id, home, away, date)
        html_table_to_sqlite(tables[10], basic_q1_schema, insert_q1_schema, game_id, home, away, date)
        html_table_to_sqlite(tables[11], basic_q2_schema, insert_q2_schema, game_id, home, away, date)
        html_table_to_sqlite(tables[12], basic_h1_schema, insert_h1_schema, game_id, home, away, date)
        html_table_to_sqlite(tables[13], basic_q3_schema, insert_q3_schema, game_id, home, away, date)
        html_table_to_sqlite(tables[14], basic_q4_schema, insert_q4_schema, game_id, home, away, date)
        html_table_to_sqlite(tables[15], basic_h2_schema, insert_h2_schema, game_id, home, away, date)
        html_table_to_sqlite(tables[16], basic_ot1_schema, insert_ot1_schema, game_id, home, away, date)
        html_table_to_sqlite(tables[17], advanced_schema, advanced_insert_schema, game_id, home, away, date)

links = ['https://www.basketball-reference.com/boxscores/202403010DET.html', 'https://www.basketball-reference.com/boxscores/202403010PHI.html', 'https://www.basketball-reference.com/boxscores/202403010BOS.html', 'https://www.basketball-reference.com/boxscores/202403010TOR.html', 'https://www.basketball-reference.com/boxscores/202403010MEM.html', 'https://www.basketball-reference.com/boxscores/202403010MIN.html', 'https://www.basketball-reference.com/boxscores/202403010NOP.html', 'https://www.basketball-reference.com/boxscores/202403010CHI.html', 'https://www.basketball-reference.com/boxscores/202403010LAC.html', 'https://www.basketball-reference.com/boxscores/202403020BRK.html', 'https://www.basketball-reference.com/boxscores/202403020MIA.html', 'https://www.basketball-reference.com/boxscores/202403020MEM.html', 'https://www.basketball-reference.com/boxscores/202403020LAL.html', 'https://www.basketball-reference.com/boxscores/202403020PHO.html', 'https://www.basketball-reference.com/boxscores/202403030DAL.html', 'https://www.basketball-reference.com/boxscores/202403030BOS.html', 'https://www.basketball-reference.com/boxscores/202403030MIN.html', 'https://www.basketball-reference.com/boxscores/202403030ORL.html', 'https://www.basketball-reference.com/boxscores/202403030TOR.html', 'https://www.basketball-reference.com/boxscores/202403030CLE.html', 'https://www.basketball-reference.com/boxscores/202403030SAS.html', 'https://www.basketball-reference.com/boxscores/202403030PHO.html', 'https://www.basketball-reference.com/boxscores/202403040BRK.html', 'https://www.basketball-reference.com/boxscores/202403040MIL.html', 'https://www.basketball-reference.com/boxscores/202403040MIN.html', 'https://www.basketball-reference.com/boxscores/202403040UTA.html', 'https://www.basketball-reference.com/boxscores/202403040SAC.html', 'https://www.basketball-reference.com/boxscores/202403040LAL.html', 'https://www.basketball-reference.com/boxscores/202403050CHO.html', 'https://www.basketball-reference.com/boxscores/202403050BRK.html', 'https://www.basketball-reference.com/boxscores/202403050CLE.html', 'https://www.basketball-reference.com/boxscores/202403050MIA.html', 'https://www.basketball-reference.com/boxscores/202403050NYK.html', 'https://www.basketball-reference.com/boxscores/202403050TOR.html', 'https://www.basketball-reference.com/boxscores/202403050HOU.html', 'https://www.basketball-reference.com/boxscores/202403050DAL.html', 'https://www.basketball-reference.com/boxscores/202403050DEN.html', 'https://www.basketball-reference.com/boxscores/202403060WAS.html', 'https://www.basketball-reference.com/boxscores/202403060ATL.html', 'https://www.basketball-reference.com/boxscores/202403060HOU.html', 'https://www.basketball-reference.com/boxscores/202403060PHI.html', 'https://www.basketball-reference.com/boxscores/202403060UTA.html', 'https://www.basketball-reference.com/boxscores/202403060GSW.html', 'https://www.basketball-reference.com/boxscores/202403060POR.html', 'https://www.basketball-reference.com/boxscores/202403060LAL.html', 'https://www.basketball-reference.com/boxscores/202403070DET.html', 'https://www.basketball-reference.com/boxscores/202403070IND.html', 'https://www.basketball-reference.com/boxscores/202403070DAL.html', 'https://www.basketball-reference.com/boxscores/202403070PHO.html', 'https://www.basketball-reference.com/boxscores/202403070DEN.html', 'https://www.basketball-reference.com/boxscores/202403070GSW.html', 'https://www.basketball-reference.com/boxscores/202403070SAC.html', 'https://www.basketball-reference.com/boxscores/202403080PHI.html', 'https://www.basketball-reference.com/boxscores/202403080WAS.html', 'https://www.basketball-reference.com/boxscores/202403080CLE.html', 'https://www.basketball-reference.com/boxscores/202403080NYK.html', 'https://www.basketball-reference.com/boxscores/202403080MEM.html', 'https://www.basketball-reference.com/boxscores/202403080OKC.html', 'https://www.basketball-reference.com/boxscores/202403080LAL.html', 'https://www.basketball-reference.com/boxscores/202403080POR.html', 'https://www.basketball-reference.com/boxscores/202403090LAC.html', 'https://www.basketball-reference.com/boxscores/202403090CHO.html', 'https://www.basketball-reference.com/boxscores/202403090DET.html', 'https://www.basketball-reference.com/boxscores/202403090GSW.html', 'https://www.basketball-reference.com/boxscores/202403090PHO.html', 'https://www.basketball-reference.com/boxscores/202403090DEN.html', 'https://www.basketball-reference.com/boxscores/202403090POR.html', 'https://www.basketball-reference.com/boxscores/202403100LAC.html', 'https://www.basketball-reference.com/boxscores/202403100ATL.html', 'https://www.basketball-reference.com/boxscores/202403100MIA.html', 'https://www.basketball-reference.com/boxscores/202403100ORL.html', 'https://www.basketball-reference.com/boxscores/202403100SAC.html', 'https://www.basketball-reference.com/boxscores/202403100CLE.html', 'https://www.basketball-reference.com/boxscores/202403100NYK.html', 'https://www.basketball-reference.com/boxscores/202403100OKC.html', 'https://www.basketball-reference.com/boxscores/202403100LAL.html', 'https://www.basketball-reference.com/boxscores/202403110DET.html', 'https://www.basketball-reference.com/boxscores/202403110CLE.html', 'https://www.basketball-reference.com/boxscores/202403110CHI.html', 'https://www.basketball-reference.com/boxscores/202403110SAS.html', 'https://www.basketball-reference.com/boxscores/202403110DEN.html', 'https://www.basketball-reference.com/boxscores/202403110POR.html', 'https://www.basketball-reference.com/boxscores/202403120NYK.html', 'https://www.basketball-reference.com/boxscores/202403120MEM.html', 'https://www.basketball-reference.com/boxscores/202403120OKC.html', 'https://www.basketball-reference.com/boxscores/202403120SAS.html', 'https://www.basketball-reference.com/boxscores/202403120UTA.html', 'https://www.basketball-reference.com/boxscores/202403120LAC.html', 'https://www.basketball-reference.com/boxscores/202403120SAC.html', 'https://www.basketball-reference.com/boxscores/202403130DET.html', 'https://www.basketball-reference.com/boxscores/202403130ORL.html', 'https://www.basketball-reference.com/boxscores/202403130IND.html', 'https://www.basketball-reference.com/boxscores/202403130MIA.html', 'https://www.basketball-reference.com/boxscores/202403130MEM.html', 'https://www.basketball-reference.com/boxscores/202403130NOP.html', 'https://www.basketball-reference.com/boxscores/202403130DAL.html', 'https://www.basketball-reference.com/boxscores/202403130POR.html', 'https://www.basketball-reference.com/boxscores/202403130SAC.html', 'https://www.basketball-reference.com/boxscores/202403140BOS.html', 'https://www.basketball-reference.com/boxscores/202403140CHI.html', 'https://www.basketball-reference.com/boxscores/202403140HOU.html', 'https://www.basketball-reference.com/boxscores/202403140MIL.html', 'https://www.basketball-reference.com/boxscores/202403140OKC.html', 'https://www.basketball-reference.com/boxscores/202403140POR.html', 'https://www.basketball-reference.com/boxscores/202403150CHO.html', 'https://www.basketball-reference.com/boxscores/202403150DET.html', 'https://www.basketball-reference.com/boxscores/202403150TOR.html', 'https://www.basketball-reference.com/boxscores/202403150NOP.html', 'https://www.basketball-reference.com/boxscores/202403150SAS.html', 'https://www.basketball-reference.com/boxscores/202403150UTA.html', 'https://www.basketball-reference.com/boxscores/202403160HOU.html', 'https://www.basketball-reference.com/boxscores/202403160IND.html', 'https://www.basketball-reference.com/boxscores/202403160NOP.html', 'https://www.basketball-reference.com/boxscores/202403160PHI.html', 'https://www.basketball-reference.com/boxscores/202403160CHI.html', 'https://www.basketball-reference.com/boxscores/202403160MEM.html', 'https://www.basketball-reference.com/boxscores/202403160LAL.html', 'https://www.basketball-reference.com/boxscores/202403160UTA.html', 'https://www.basketball-reference.com/boxscores/202403160SAC.html', 'https://www.basketball-reference.com/boxscores/202403170MIL.html', 'https://www.basketball-reference.com/boxscores/202403170DET.html', 'https://www.basketball-reference.com/boxscores/202403170DAL.html', 'https://www.basketball-reference.com/boxscores/202403170ORL.html', 'https://www.basketball-reference.com/boxscores/202403170WAS.html', 'https://www.basketball-reference.com/boxscores/202403170SAS.html', 'https://www.basketball-reference.com/boxscores/202403170LAC.html', 'https://www.basketball-reference.com/boxscores/202403180IND.html', 'https://www.basketball-reference.com/boxscores/202403180BOS.html', 'https://www.basketball-reference.com/boxscores/202403180PHI.html', 'https://www.basketball-reference.com/boxscores/202403180CHI.html', 'https://www.basketball-reference.com/boxscores/202403180UTA.html', 'https://www.basketball-reference.com/boxscores/202403180GSW.html', 'https://www.basketball-reference.com/boxscores/202403180SAC.html', 'https://www.basketball-reference.com/boxscores/202403180LAL.html', 'https://www.basketball-reference.com/boxscores/202403190ORL.html', 'https://www.basketball-reference.com/boxscores/202403190WAS.html', 'https://www.basketball-reference.com/boxscores/202403190BRK.html', 'https://www.basketball-reference.com/boxscores/202403190SAS.html', 'https://www.basketball-reference.com/boxscores/202403190MIN.html', 'https://www.basketball-reference.com/boxscores/202403200CLE.html', 'https://www.basketball-reference.com/boxscores/202403200DET.html', 'https://www.basketball-reference.com/boxscores/202403200BOS.html', 'https://www.basketball-reference.com/boxscores/202403200TOR.html', 'https://www.basketball-reference.com/boxscores/202403200OKC.html', 'https://www.basketball-reference.com/boxscores/202403200GSW.html', 'https://www.basketball-reference.com/boxscores/202403200PHO.html', 'https://www.basketball-reference.com/boxscores/202403200POR.html']

[run_script(link) for link in links]
# run_script('https://www.basketball-reference.com/boxscores/202310270CHI.html')

