# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

# coding: utf-8

# coding: utf-8
"""
Post the query to Google　Search and get the return results
"""
# import urllib3
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import csv
import lxml
#
# class Crawler:
#     def getPage(self,url):
#         USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
#         headers = {"user-agent" : USER_AGENT}
#
#         try:
#             req = requests.get(url, headers = headers)
#
#         except requests.exceptions.RequestException:
#
#             return None
#         else:
#             if req.status_code == 200:
#                 return BeautifulSoup(req.text, "html.parser")
#
#
#     def search(self, site):
#
#         try :
#             bs = self.getPage(site)
#             topic = "AA"
#             title = "BB"
#             body = "C"
#             content = Content(topic, site, title, body)
#             content.save()
#         except :
#             print("Something was wrong with that page or Url. Skipping!")


companies = ['Analog+Technology','hon+hai']
searchResults = []

# Browser settings
chrome_options = Options()
chrome_options.add_argument('--incognito')
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0')
browser = webdriver.Chrome(chrome_options=chrome_options)
# crawler = Crawler()

for comp in companies:
# Query settings
    csvFile = open("{}.csv".format(comp), "w+", newline = "")
    writer = csv.DictWriter(csvFile, fieldnames = ["url", "title", "body"])
    writer.writeheader()
    csvFile.close
    query = comp
    control = True
    browser.get("https://patents.google.com/?assignee="
                + query+ "&country=US&before=priority:20141231&after=priority:20140101&oq=assignee:("+ query +")+country:US+before:priority:20141231+after:priority:20140101")
    # next_page_times = 10
    # Crawler
    while control:
        # time.sleep(5)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        content = soup.prettify()
        # print(content)
        # urls = re.findall(r'href=.+(/patent/)', content)
        # print(urls)
        searchResults.extend(soup.select('[href^="/patent/"]'))
        print(searchResults)

        for result in searchResults:
            print(result["href"])
        # Get titles and urls
        # titles = re.findall('<h3 class="[\w\d]{6} [\w\d]{6}">\n +(.+)', content)
        # urls = re.findall('<div class="r"> *\n *<a href="(.+)" onmousedown', soup.prettify())

        # for n in range(min(len(titles), len(urls))):
        #     # print(titles[n], urls[n])

        # Turn to the next page
        try:
            # browser.find_element_by_xpath("//*[@id='link']/paper-icon-button[@icon='chevron-right']").click()
            browser.find_element_by_css_selector("paper-icon-button[icon='chevron-right']").click()
            #Wait
            time.sleep(3)
        except:
            print('Next Company')
            control = False

browser.close()