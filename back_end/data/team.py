import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from io import StringIO

 
def extract_team_name_from_link(link):
    pattern = r'/teams/([A-Z]+)/'
    match = re.search(pattern, link)
    if match:
        team_name = match.group(1)
        return team_name
    else:

        return None

def get_web_element_by_id(link,element_id, driver=webdriver.Firefox()):
    driver.get(link)
    WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.ID, element_id))
    )
    return driver.find_element(By.ID, element_id)


def get_html_from_web_element(web_element):
    return web_element.get_attribute('outerHTML')


def html_to_pandas_table(html):
    return pd.read_html(StringIO(html))   
 
    
def write_table_to_csv(link,table,name):
    team = extract_team_name_from_link(link)
    table[0].to_csv(f'team_tables_csv/{team}/{team}_{name}.csv', index=False)
    print(f"wrote {team} {name.capitalize()} table to csv...")

 
def run_script(link, driver=webdriver.Firefox()):
    element_ids = ["team_misc", "roster"]
    for element_id in element_ids:
        web_element = get_web_element_by_id(link,element_id)
        html = get_html_from_web_element(web_element)
        table = html_to_pandas_table(html)
        write_table_to_csv(link, table, element_id.capitalize())
        driver.quit() 


if __name__ == "__main__":
    # link = "https://www.basketball-reference.com/teams/NYK/2024.html"
    # run_script(link)
    links = ["https://www.basketball-reference.com/teams/ATL/2024.html",
             "https://www.basketball-reference.com/teams/BOS/2024.html",
             "https://www.basketball-reference.com/teams/PHI/2024.html",
             "https://www.basketball-reference.com/teams/BRK/2024.html",
             "https://www.basketball-reference.com/teams/TOR/2024.html",
             "https://www.basketball-reference.com/teams/CLE/2024.html",
             "https://www.basketball-reference.com/teams/MIL/2024.html",
             "https://www.basketball-reference.com/teams/IND/2024.html",
             "https://www.basketball-reference.com/teams/CHI/2024.html",
             "https://www.basketball-reference.com/teams/DET/2024.html",
             "https://www.basketball-reference.com/teams/ORL/2024.html",
             "https://www.basketball-reference.com/teams/MIA/2024.html",
             "https://www.basketball-reference.com/teams/CHO/2024.html",
             "https://www.basketball-reference.com/teams/WAS/2024.html",
             "https://www.basketball-reference.com/teams/MIN/2024.html",
             "https://www.basketball-reference.com/teams/OKC/2024.html",
             "https://www.basketball-reference.com/teams/DEN/2024.html",
             "https://www.basketball-reference.com/teams/UTA/2024.html",
             "https://www.basketball-reference.com/teams/POR/2024.html",
             "https://www.basketball-reference.com/teams/LAC/2024.html",
             "https://www.basketball-reference.com/teams/SAC/2024.html",
             "https://www.basketball-reference.com/teams/PHO/2024.html",
             "https://www.basketball-reference.com/teams/LAL/2024.html",
             "https://www.basketball-reference.com/teams/GSW/2024.html",
             "https://www.basketball-reference.com/teams/NOP/2024.html",
             "https://www.basketball-reference.com/teams/DAL/2024.html",
             "https://www.basketball-reference.com/teams/HOU/2024.html",
             "https://www.basketball-reference.com/teams/MEM/2024.html",
             "https://www.basketball-reference.com/teams/SAS/2024.html",
             "https://www.basketball-reference.com/teams/NYK/2024.html"]
    [run_script(link) for link in links]
    







