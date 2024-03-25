import pandas as pd
import sqlite3

url = 'sqlite:///C:/Users/thabi/Documents/BBallAI/back_end/data/nba_databases/NBA.db'
url_ = 'sqlite:///C:/Users/thabi/Documents/BBallAI/back_end/data/nba_databases/nba.db'



def connect_to_database(url):
    conn = sqlite3.connect(url)
    return conn
# Read the SQLite table into a Pandas DataFrame


def select_all_from_table(table_name):
    query = "SELECT * FROM table_name"
    return query


def dataframe_from_sql_query(query, connection):
    df = pd.read_sql_query(query, connection)
    return df


columns_to_convert = ['true_shooting_pct', 'effective_FG_pct', '_3p_attempts_rate', 'ft_rate', 'offensive_rebound_pct',
                      'defensive_rebound_pct', 'total_rebound_pct', 'assist_pct', 'block_pct', 'turnover_pct',
                      'usage_pct' ]  # Specify columns to convert

''' advanced[
player_name, minutes, true_shooting_pct, effective_fg_pct, 
_3p_attempts_rate, ft_rate, offensive_rebound_pct, defensive_rebound_pct,
total_rebound_pct, assist_pct, steal_pct, block_pct, turnover_pct,
usage_pct, offensive_rating, defensive_rating, box_plus_minus,Tteam_id,
time_frame, table_type, away_team_id, home_team_id, game_date,
game_info, game_id]'''
def convert_columns_to_ints(df, new_table, conn, columns_to_convert):
    for column in columns_to_convert:
        df[column] = pd.to_numeric(df[column], errors='coerce')  # Convert to numeric, coerce errors to NaN
    # Write the modified DataFrame back to the SQLite database, replacing the existing table
    df.to_sql(new_table, conn, if_exists='replace', index=False)
    conn.close()

def run_query(first_url, sec_url, columns_to_convert):
    connection = connect_to_database(first_url)
    query = select_all_from_table('advanced_game')
    df = dataframe_from_sql_query(query, connection)
    conn = connect_to_database(sec_url)
    convert_columns_to_ints(df, 'advanced', conn, columns_to_convert)

run_query(url, url_, columns_to_convert)