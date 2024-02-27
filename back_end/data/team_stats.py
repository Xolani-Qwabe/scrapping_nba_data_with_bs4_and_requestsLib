import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Scrape_Team_Stats:
    
    
    def __init__(self, link, driver=webdriver.Firefox()):
        self.link = link
        self.driver = driver
        self.build()
        
        
        
    def extract_team_name_from_link(self):
        pattern = r'/teams/([A-Z]+)/'
        match = re.search(pattern, self.link)
        if match:
            team_name = match.group(1)
            return team_name
        else:

            return None
        
    def get_web_element_by_id(self, table_id):
        self.driver.get(self.link)
        WebDriverWait(self.driver, 40).until(
    EC.presence_of_element_located((By.ID, table_id))
    )
        return self.driver.find_element(By.ID, table_id)
        
        
    def get_html_from_web_element(self):
        web_element = self.get_html_from_web_element()
        return web_element.get_attribute('outerHTML')
    
    
    def html_to_pandas_table(self):
        html = self.get_html_from_web_element()
        return pd.read_html(html)    
    
    
    def write_table_to_csv(self):
        team = self.extract_team_name_from_link(self.link)
        table = self.html_to_pandas_table()
        table[0].to_csv(f'{team}_{self.h}.csv', index=False)
        print(f"wrote {team} {self.table_id.capitalize()} table to csv...")
        self.driver.quit()
         
       
   
   
    def build(self):
        element_ids = ["salaries2", "pbp", "shooting", "adj_shooting", "advanced", "per_poss", "per_minute", "totals", "per_game", "team_misc", "team_and_opponent", "roster", "injuries"]
        for element_id in element_ids:
            self.get_web_element_by_id(element_id)
            self.get_html_from_web_element()
            self.html_to_pandas_table()
            self.write_table_to_csv()
        
            

   
