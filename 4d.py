import requests
import os.path
import sys
from pathlib import Path

from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime
from pymongo import MongoClient

# URLS
url = "http://www.singaporepools.com.sg/en/product/Pages/4d_results.aspx"

# MongoDB Connection
client = MongoClient('localhost', 27017)
db = client.lottery
collection = db.fourd

# Functions
def getPage(mode):
    # Start Selenium browser get page
    browser = webdriver.Chrome()
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, "html.parser")

    # Find Filepath
    if(mode == "test"):
        processPage(soup,mode)
    else:
        mainPath = os.path.dirname(os.path.realpath(__file__))
        resultsPath = "output/4d"
        i = datetime.now()
        filename = i.strftime('%Y%m%d%H%M%S') + ".txt"
        filepath = os.path.join(mainPath, resultsPath, filename)

        # Write result to file
        try:
            with open(filepath, "w",encoding="utf-8") as file:
                print("file created at " + filepath + "\n")
                file.write(str(soup))
                file.close()
                processPage(soup,mode)
        except IOError:
            print("Unable to write to file")
    return

def processPage(soup, mode):

    #Top Results Table Processing
    topTable = soup.find("table",{"class":"table table-striped orange-header"})
    rawDrawDate = topTable.find("th",{"class":"drawDate"}).get_text()

    #Draw Date & Draw Number
    drawDate = datetime.strptime(rawDrawDate[5:],'%d %b %Y').strftime('%Y%m%d')
    rawDrawNumber = topTable.find("th",{"class":"drawNumber"}).get_text()
    drawNumber = rawDrawNumber[9:]
    print("Draw Date " + drawDate)
    print("Draw Number " + drawNumber + "\n")
    print("Top 3 Numbers")

    #Storage list for all results
    top = []
    starter = []
    consolation = []

    #Top Results
    for row in topTable.findAll('tr'):
        tableDatas = row.findAll('td')
        for tableData in tableDatas:
            print(tableData.get_text())
            top.append(tableData.get_text())

    print("Starter Numbers")
    #Starter Results Table Processing
    starterTable = soup.find("tbody",{"class":"tbodyStarterPrizes"})
    for row in starterTable.findAll('tr'):
        columns = row.findAll('td')
        for column in columns:
            print(column.get_text())
            starter.append(column.get_text())
            #if auto store data

    print("Consolation Numbers")
    #Consolation Results table Processing
    consolTable = soup.find("tbody",{"class":"tbodyConsolationPrizes"})
    for row in consolTable.findAll('tr'):
        columns = row.findAll('td')
        for column in columns:
            print(column.get_text())
            consolation.append(column.get_text())
            #if auto store data

    if(mode == "auto"):
        storeData(drawDate, drawNumber, top, starter, consolation)

def storeData(drawDate, drawNumber, top, starter, consolation):
    print("Inserting into MongoDB")
    #Insert String
    insertJSON = {"drawNumber": drawNumber,
    "drawDate": drawDate,
    }

    i = 0
    for result in top:
        insertJSON["t"+str(i)] = result
        i += 1

    for result in starter:
        insertJSON["s"+str(i)] = result
        i += 1

    for result in consolation:
        insertJSON["c"+str(i)] = result
        i += 1

    print(insertJSON)
    collection.insert_one(insertJSON)



#Print argument error
def argError():
    print("Argument error. Enter only the available case sensitive commands")
    print("python 4d.py auto")
    print("python 4d.py test")
    print("python 4d.py read path/to/file")

#Main
if(len(sys.argv) < 2):
    argError()
    exit()
else:
    # Modes are presented by "auto", "test", "read"
    mode = sys.argv[1]
    print(mode +" mode selected \n")
    if(mode == "auto" or mode =="test"):
        getPage(mode)
        exit()
    elif(mode == "read"):
        try:
            filepath = Path(sys.argv[2])
            if filepath.is_file():
                html_report = open(filepath,'r',encoding="utf-8").read()
                soup = BeautifulSoup(html_report, "html.parser")
                processPage(soup, mode)
            else:
                print("File path is invalid")
        except Exception as e:
            print(e)
            argError()
    else:
        argError()
