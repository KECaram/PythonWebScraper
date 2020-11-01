#!/usr/bin/python
# Keith Caram
# INFO.305.061: Survey of Python, Perl, and PHP
# Assignment #5 - Python Web App
#                               Program Summary
#This is a tiny bit of test code. I wrote test code that checks if my home page loads
#and that the page loads with the correct header.

import unittest
from WebScraper import app
import unittest

class webScraperAppTest(unittest.TestCase):

    def test_home(self):
        tester = app.test_client(self)
        response = tester.get('/')
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_home_content(self):
            tester = app.test_client(self)
            response = tester.get('/', content_type= 'html/text')
            self.assertTrue(b'Book Scraper' in response.data)



if __name__ == '__main__':
    unittest.main()