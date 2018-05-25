# lottery-scraper
Lottery Scraping(PYTHON)  

This tool is created to provide 4D/TOTO results.  

# Requirements
Python 3.63 - Scraper Programming Language  
Selenium - Browser  
BeautifulSoup - HTML/XML Parser  
Requests - For get request
MongoDB - NoSQL Database  
Laravel - API / Site  
PHP - Laravel  
Atom - Text Editor  

# Installation
BeautifulSoup Installation
python -m pip install beautifulsoup4

Selenium   
Download ChromeDriver - https://chromedriver.storage.googleapis.com/index.html?path=2.38/  
Create folder in C://webdrivers and place downloaded file in  
Add C://webdrivers into Path of System Environment Variables  
python -m pip install Selenium

Requests
python -m pip install requests

# Updates
Get page using BeautifulSoup/Selenium
Sanitize Results
Created modes

# TODO
Server Setup  
Setup MongoDB   
Pass results into MongoDB  
API via Laravel  
Telegram Bot?  
Android App?  

# Run instructions
There are 3 main modes to select. The auto mode get and write the scraped site's content to the output folder and it will store the extracted results into the database and print the values to console. The test mode does the same however it does not write the scraped site's content to the output folder. The read mode will extract the results from an existing file.

python lotter.py auto
python lotter.py test
python lotter.py read output/filepath.txt
