import unittest
from unittest.mock import MagicMock, patch
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import scrapping_stats.get_box_scores as get_box_scores_var

class TestMainFunctions(unittest.TestCase):

    def setUp(self):
        self.sample_html = '<html><head></head><body><div id="content"><h1>Game Details</h1></div></body></html>'
        self.mock_response = MagicMock()
        self.mock_response.content = self.sample_html

    @patch('main.requests.get')
    def test_get_html_page(self, mock_get):
        mock_get.return_value = self.mock_response
        result = get_box_scores_var.get_html_page('https://example.com')
        self.assertIsInstance(result, BeautifulSoup)

    @patch('main.requests.get')
    def test_get_html_pages(self, mock_get):
        mock_get.return_value = self.mock_response
        result = get_box_scores_var.get_html_pages(['https://example.com'])
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], BeautifulSoup)

    # Add more test methods for other functions...

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
