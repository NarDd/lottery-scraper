import requests
import os.path

from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime

# URLS
url = "http://www.singaporepools.com.sg/en/product/Pages/4d_results.aspx"

# Start Selenium browser get page
browser = webdriver.Chrome()
browser.get(url)
soup = BeautifulSoup(browser.page_source, "html.parser")

# Find Filepath
mainPath = os.path.dirname(os.path.realpath(__file__))
resultsPath = "output"
i = datetime.now()
print(i.strftime('%Y%m%d%H%M%S'))
filename = i.strftime('%Y%m%d%H%M%S') + ".txt"
filepath = os.path.join(mainPath, resultsPath, filename)

# Write result to file
try:
    with open(filepath, "w",encoding="utf-8") as file:
        file.write(str(soup))
except IOError:
    print("Unable to write to file")
