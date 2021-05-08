from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import csv

companies = []
chrome_options = Options()
chrome_options.add_argument('--incognito')
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0')
browser = webdriver.Chrome(chrome_options=chrome_options)


class searchTerm:
    def __init__(self, date, name):
        self.date = date
        self.name = name

csvFile1 = open("compatent.csv", "w+", newline = "")
try:
    writer = csv.DictWriter(csvFile1, fieldnames = ["st", "search term", "url", "date", "title", "assignee", "cited by"])
    writer.writeheader()
finally:
    csvFile1.close()

with open("/Users/Howard/Desktop/ST.csv", newline="", encoding= "UTF-8-sig") as compdata:
    rows = csv.reader(compdata, delimiter = ",")

    for row in rows:
        companies.append(searchTerm(row[0], row[1]))





class Content:

    def __init__(self, topic, url, title, body, date, query ,st):
        self.topic = topic
        self.title = title
        self.body = body
        self.url = url
        self.date = date
        self.query = query
        self.st = st

    def print(self):

        print("New article found for topic: {}".format(self.topic))
        print("URL: {}".format(self.url))
        print("TITLE: {}".format(self.title))
        print("BODY: \n{}".format(self.body))

    def save(self):
        csvFile = open("compatent.csv", "a+", newline = "")
        try:

            writer =csv.writer(csvFile)
            writer.writerow( [self.st , self.query, self.url ,self.date, self.topic , self.body ,self.title])

        finally:
            csvFile.close()

class Crawler:
    def getPage(self,url):
        USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
        headers = {"user-agent" : USER_AGENT}

        try:
            req = requests.get(url, headers = headers)

        except requests.exceptions.RequestException:

            return None
        else:
            if req.status_code == 200:
                return BeautifulSoup(req.text, "lxml")


    def search(self, site, query, period):

        try :
            browser.get(site)
            element = WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".patent-result")))
            bs = BeautifulSoup(browser.page_source, 'lxml')
            topic = bs.select("title")
            title = bs.find("h3", id = "citedBy")
            # print(title)
            # title = title.string
            body = bs.find("span", id = "assigneeWarning").find_parent("dt").find_next_siblings("dd")
            date = bs.find(class_="priority style-scope application-timeline").string
            # print(date)
            content = Content(topic, site, title, body, date, query, period)
            # content.print()
            content.save()
        except Exception as ellol :
            print(ellol)


def PatentCrawler(date, query):
    results = []
    period = str(int(date) + 2)
    selector = "paper-icon-button[icon='chevron-right']"
    # // *[ @ id = "link"] / paper - icon - button
    browser.get("https://patents.google.com/?assignee="
                + query + "&country=US&before=priority:" + period + "1231&after=priority:" + period + "0101&oq=assignee:(" + query + ")+country:US+before:priority:" + period + "1231+after:priority:" + period + "0101")

    while True:
        try:

            element = WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,selector)))
            # element = WebDriverWait(browser, 10).until(EC.presence_of_element_located(By.css,"paper-icon-button[icon='chevron-right']"))
        except Exception as other:
            print(other)

        soup = BeautifulSoup(browser.page_source, 'lxml')
        results.extend(soup.find_all("state-modifier", attrs={"data-result": True}))

        try:
            browser.find_element_by_css_selector("paper-icon-button[icon='chevron-right']").click()
        except Exception as error:
            print(error)
            break
    return results


Crawler = Crawler()
for comp in companies:
# Query settings

    searchResults = PatentCrawler(comp.date, comp.name)

    for result in searchResults:
        Crawler.search("https://patents.google.com/" + result["data-result"], comp.name, comp.date)
    #     print(result["data-result"])
    #     cResults.append(result["data-result"])
    # cResults = set(cResults)
    # print(len(cResults))

browser.close()

