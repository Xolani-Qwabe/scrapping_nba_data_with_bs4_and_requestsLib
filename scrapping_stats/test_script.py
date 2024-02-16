import requests
from bs4 import BeautifulSoup
import time
import regex as r
from datetime import datetime

url= 'https://www.basketball-reference.com/boxscores/202402140UTA.html'

def send_request_for_one_html_page_to_site(url):
    """Handles HTTP Status Code errors"""
    try:
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0'
        })
        response.raise_for_status()  # Raises an HTTPError for bad responses
        print("Thread going to sleep for 5 seconds request sent")
        time.sleep(5)
        return BeautifulSoup(response.content, 'html.parser')
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

print(send_request_for_one_html_page_to_site(url))