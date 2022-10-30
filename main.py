import time
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup

#URL = "https://www.swimrankings.net/index.php?page=athleteDetail&athleteId=4359097"
URL = "https://www.swimrankings.net/index.php?page=athleteDetail&athleteId=4844975"
strona = requests.get(URL)

soup = BeautifulSoup(strona.content, "html.parser")

wynik = soup.find_all("table", class_="athleteBest")

krotki_basen = soup.find_all("tr", class_="athleteBest0")
data_list = []
count = 0
for result in krotki_basen:
    event = result.find("td", class_="event")
    event_text = event.text
    count += 1
    print(count)
    link = event.find("a")
    time.sleep(3)
    link = "https://www.swimrankings.net/index.php" + link['href']
    page = requests.get(link)
    zupka = BeautifulSoup(page.content, "html.parser")
    data = zupka.find_all("table", class_="athleteRanking")
    for element in data:
        linijki = element.find_all("tr")
        pol = ""
        num = 0
        for row in linijki:
            czasy = []
            num += 1
            print(num)
            if row["class"][0] == 'athleteRankingHead':
                pol = row.text
            else:
                czasy.append(event_text)
                czasy.append(pol)
                times = row.find("td", class_="time")
                p = times.find("a")['href']
                time.sleep(3)
                redi = "https://www.swimrankings.net/index.php" + times.find("a")['href']
                redi_page = requests.get(redi)
                redi_soup = BeautifulSoup(redi_page.content, "html.parser")
                club = 0
                if redi_soup.find_all("td", class_="right") != []:
                    club = redi_soup.find_all("td", class_="right")[1].text
                czasy.append(times.text)
                code = row.find("td", class_="code").text
                czasy.append(code)
                date = row.find("td", class_="date").text
                czasy.append(date)
                city = row.find("td", class_="city").text
                czasy.append(city)
                czasy.append(club)
                data_list.append(czasy)
df = pd.DataFrame(data_list)
df.columns = ['event', 'pool', 'time', 'points', 'date', 'city', 'club']
print(df.head())
df.to_csv('athlete.csv')

