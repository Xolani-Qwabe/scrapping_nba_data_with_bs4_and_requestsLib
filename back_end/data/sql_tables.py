from bs4 import BeautifulSoup
import requests
import time
import sqlite3


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

def html_table_to_sqlite(html_table):
    rows = html_table.find_all('tr')
    conn = sqlite3.connect('new_stats.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS GSW_basicH2 
                    (Player TEXT, MP TEXT, FG INTEGER, FGA INTEGER, FG_PCT TEXT, 
                    FG3 INTEGER, FG3A INTEGER, FG3_PCT TEXT, FT INTEGER, FTA INTEGER, 
                    FT_PCT TEXT, ORB INTEGER, DRB INTEGER, TRB INTEGER, AST INTEGER, 
                    STL INTEGER, BLK INTEGER, TOV INTEGER, PF INTEGER, PTS INTEGER, 
                    PLUS_MINUS TEXT)''')
    for row in rows[2:]:
        print(len(row))
        print(row)
        cols = row.find_all(['th', 'td'])
        values = [col.get_text() for col in cols]
        if len(values) == 21:  # ensure we have all columns filled
            cursor.execute('INSERT INTO GSW_basicH2  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', values)

    # Commit changes and close connection
    conn.commit()
    conn.close()



tables = get_all_tables(send_request_for_one_html_page_to_site('https://www.basketball-reference.com/boxscores/202402010BOS.html'))
# print((tables[8]))
# # write_html_tables_to_sqlite(tables[10])
html_table_to_sqlite(tables[14])

