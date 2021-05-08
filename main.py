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
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    searchResults = []
    csvFile = open("{}.csv".format(comp), "w+", newline = "")
    writer = csv.DictWriter(csvFile, fieldnames = ["url", "title", "body"])
    writer.writeheader()
    csvFile.close
    query = comp
    control = True
    browser.get("https://patents.google.com/?assignee="
                + query + "&country=US&before=priority:20141231&after=priority:20140101&oq=assignee:("+ query +")+country:US+before:priority:20141231+after:priority:20140101")
    # next_page_times = 10
    # Crawler
    while control:


        # content = soup.prettify()
        # print(content)
        # urls = re.findall(r'href=.+(/patent/)', content)
        # print(urls)
        # searchResults.extend(soup.select('[href^="/patent/"]'))
        try:
            element = WebDriverWait(browser, 10).until(EC.presenceOfElementLocated(By.name("search-result-item")))
        except:
            print("not get")

        soup = BeautifulSoup(browser.page_source, 'lxml')
        searchResults.extend(soup.find_all("state-modifier",attrs={"data-result" : True}))


        # for result in searchResults:
        #     print(result["href"])
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
            # myDynamicElement = browser.find_element_by_id("myDynamicElement")
        except:
            i = 0
            print('Next Company')
            for result in searchResults:
                i = i+1
                print(result["data-result"])
            print(i)
            control = False


# class Content:
#
#     def __init__(self, topic, url, title, body):
#         self.topic = topic
#         self.title = title
#         self.body = body
#         self.url = url
#
#     def print(self):
#
#         print("New article found for topic: {}".format(self.topic))
#         print("URL: {}".format(self.url))
#         print("TITLE: {}".format(self.title))
#         print("BODY: \n{}".format(self.body))
#
#     def save(self):
#         csvFile = open("{}.csv".format(self.topic), "a+", newline = "")
#         try:
#
#             writer =csv.writer(csvFile)
#             writer.writerow( [self.url, self.title, self.body])
#
#         finally:
#             csvFile.close

# class Website:
#     def __init__(self, name, url, searchUrl, resultListing, resultUrl, absoluteUrl, titleTag, bodyTag):
#         self.name = name
#         self.url = url
#         self.searchUrl = searchUrl
#         self.resultListing = resultListing
#         self.resultUrl = resultUrl
#         self.absoluteUrl = absoluteUrl
#         self.titleTag = titleTag
#         self.bodyTag = bodyTag

# Close the browser
browser.close()