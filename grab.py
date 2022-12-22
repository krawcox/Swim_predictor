import time
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup

URL_loc ="https://www.swimrankings.net/index.php"
URL = "https://www.swimrankings.net/index.php?page=athleteDetail&athleteId=4359097"
Year_extension = "&result="

strona = requests.get(URL)

soup = BeautifulSoup(strona.content, "html.parser")
name = soup.find("div", id="name").text
name = name.split()

last_name = name[0][:-1]
first_name = name[1]
birth_year = name[2][1:]
selectors = soup.find_all("select")

years =[]
for option in selectors[-1]:
    try:
        years.append(int(option.text))
    except:
        pass
for year in years:
    page = requests.get(URL+Year_extension+str(year))
    zupka = BeautifulSoup(page.content, 'html.parser')
    results = zupka.find_all('table', class_='twoColumns')
    for element in results:
        print(element.text)