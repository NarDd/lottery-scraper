import requests
import os.path

from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime

# URLS
url = "http://www.singaporepools.com.sg/en/product/Pages/4d_results.aspx"

# Functions
def getPage():
    # Start Selenium browser get page
    browser = webdriver.Chrome()
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, "html.parser")

    # Find Filepath
    mainPath = os.path.dirname(os.path.realpath(__file__))
    resultsPath = "output"
    i = datetime.now()
    filename = i.strftime('%Y%m%d%H%M%S') + ".txt"
    filepath = os.path.join(mainPath, resultsPath, filename)

    # Write result to file
    try:
        with open(filepath, "w",encoding="utf-8") as file:
            file.write(str(soup))
    except IOError:
        print("Unable to write to file")

    processPage(soup,filepath)
    return

def processPage(soup,filepath):
    html_report = open(filepath,'r',encoding="utf-8").read()
    #soup = BeautifulSoup(html_report, "html.parser")

    #Top Results Table Processing
    topTable = soup.find("table",{"class":"table table-striped orange-header"})
    rawDrawDate = topTable.find("th",{"class":"drawDate"}).get_text()

    #Draw Date & Draw Number
    drawDate = datetime.strptime(rawDrawDate[5:],'%d %b %Y').strftime('%Y%m%d')
    rawDrawNumber = topTable.find("th",{"class":"drawNumber"}).get_text()
    drawNumber = rawDrawNumber[9:]
    print("Draw Date")
    print(drawDate)
    print("Draw Number")
    print(drawNumber)
    print("Top 3 Numbers")
    #Top Results
    for row in topTable.findAll('tr'):
        tableDatas = row.findAll('td')
        for tableData in tableDatas:
            print(tableData.get_text())

    print("Starter Numbers")
    #Starter Results Table Processing
    starterTable = soup.find("tbody",{"class":"tbodyStarterPrizes"})
    for row in starterTable.findAll('tr'):
        columns = row.findAll('td')
        for column in columns:
            print(column.get_text())

    print("Consolation Numbers")
    #Consolation Results table Processing
    consolTable = soup.find("tbody",{"class":"tbodyConsolationPrizes"})
    for row in consolTable.findAll('tr'):
        columns = row.findAll('td')
        for column in columns:
            print(column.get_text())

def Test():
    html_report = open('20180521064435.html','r',encoding="utf-8").read()
    soup = BeautifulSoup(html_report, "html.parser")

    #Top Results Table Processing
    topTable = soup.find("table",{"class":"table table-striped orange-header"})
    rawDrawDate = topTable.find("th",{"class":"drawDate"}).get_text()

    #Draw Date & Draw Number
    drawDate = datetime.strptime(rawDrawDate[5:],'%d %b %Y').strftime('%Y%m%d')
    rawDrawNumber = topTable.find("th",{"class":"drawNumber"}).get_text()
    drawNumber = rawDrawNumber[9:]
    print(drawDate)
    print(drawNumber)

    #Top Results
    for row in topTable.findAll('tr'):
        tableDatas = row.findAll('td')
        for tableData in tableDatas:
            print(tableData.get_text())

    #Starter Results Table Processing
    starterTable = soup.find("tbody",{"class":"tbodyStarterPrizes"})
    for row in starterTable.findAll('tr'):
        columns = row.findAll('td')
        for column in columns:
            print(column.get_text())

    #Consolation Results table Processing
    consolTable = soup.find("tbody",{"class":"tbodyConsolationPrizes"})
    for row in consolTable.findAll('tr'):
        columns = row.findAll('td')
        for column in columns:
            print(column.get_text())

    allTable = str(topTable) + str(starterTable) + str(consolTable)
    try:
        with open("testoutput.txt", "w",encoding="utf-8") as file:
            file.write(str(allTable))
    except IOError:
        print("Unable to write to file")
    return

# Main
getPage()
#Test()
