
import requests


import re
import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup


class Content:

    def __init__(self, topic, url, title, body):
        self.topic = topic
        self.title = title
        self.body = body
        self.url = url

    def print(self):

        print("New article found for topic: {}".format(self.topic))
        print("URL: {}".format(self.url))
        print("TITLE: {}".format(self.title))
        print("BODY: \n{}".format(self.body))

    def save(self):
        csvFile = open("{}.csv".format(self.topic), "a+", newline = "")
        try:

            writer =csv.writer(csvFile)
            writer.writerow( [self.url, self.title, self.body])

        finally:
            csvFile.close

class Website:
    def __init__(self, name, url, searchUrl, resultListing, resultUrl, absoluteUrl, titleTag, bodyTag):
        self.name = name
        self.url = url
        self.searchUrl = searchUrl
        self.resultListing = resultListing
        self.resultUrl = resultUrl
        self.absoluteUrl = absoluteUrl
        self.titleTag = titleTag
        self.bodyTag = bodyTag

class Crawler:

    def getPage(self,url):


        try:
            req = requests.get(url, headers = headers)
            print("get")


        except requests.exceptions.RequestException:

            return None
        else:
            if req.status_code == 200:
                return BeautifulSoup(req.text, 'lxml')


    def safeGet(self,pageObj,selector):
        childObj = pageObj.select(selector)
        if childObj is not None and len(childObj) > 0:
            return childObj[0].get_text()
        return ""

    def search(self, topic, site):

        bs = self.getPage(site.searchUrl + topic +"&country=US&before=priority:20141231&after=priority:20140101&oq=assignee:(" + topic + ")+country:US+before:priority:20141231+after:priority:20140101")
        searchResults = []
        p = 0
        while bs:
            searchResults.extend(bs.select(site.resultListing))


            p+= 1
            bs = self.getPage(site.searchUrl + topic +"&country=US&before=priority:20141231&after=priority:20140101&oq=assignee:(" + topic + ")+country:US+before:priority:20141231+after:priority:20140101page=" + str(p) )
            time.sleep(3)

        csvFile = open("{}.csv".format(topic), "w+", newline = "")
        writer = csv.DictWriter(csvFile, fieldnames = ["url", "title", "body"])
        writer.writeheader()
        csvFile.close
        for result in searchResults:
            url = result.select(site.resultUrl)[0].attrs["href"]

            if(site.absoluteUrl):
                bs = self.getPage(url)
            else:
                bs = self.getPage(site.url + url)
            if bs is None:
                print("Something was wrong with that page or Url. Skipping!")
                continue
            title = self.safeGet(bs,site.titleTag)
            body = self.safeGet(bs,site.bodyTag)
            if title !="" and body !="" :
                content = Content(topic,url,title,body)
                content.save()

crawler = Crawler()

siteData = [
    ["Google Patent","https://patents.google.com/","https://patents.google.com/?assignee=","#section.search-result-item.search-results","div.result-title a",False,"result-title",
    "div.patent-result"]
    ]

sites = []
for row in siteData:
    sites.append(Website(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]))

topics = ["Analog+Technology",""]
for topic in topics:
    print("GETTING INFO ABOUT: " + topic)
    for targetSite in sites:
        crawler.search(topic,targetSite)


