
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup

URL = "https://www.swimrankings.net/index.php?page=athleteDetail&athleteId=4359097"

strona = requests.get(URL)

soup = BeautifulSoup(strona.content, "html.parser")

wynik = soup.find_all("table", class_="athleteBest")

krotki_basen = soup.find_all("tr", class_="athleteBest0")
data_list = []
for result in krotki_basen:
    event = result.find("td", class_="event")
    event_text = event.text
    link = event.find("a")
    link = "https://www.swimrankings.net/index.php" + link['href']
    page = requests.get(link)
    zupka = BeautifulSoup(page.content, "html.parser")
    data = zupka.find_all("table", class_="athleteRanking")
    for element in data:
        linijki = element.find_all("tr")
        pol = ""
        for row in linijki:
            czasy = []
            if row["class"][0] == 'athleteRankingHead':
                pol = row.text
            else:
                czasy.append(event_text)
                czasy.append(pol)
                time = row.find("td", class_="time")
                p = time.find("a")['href']
                print(p)
                redi = "https://www.swimrankings.net/index.php" + time.find("a")['href']
                redi_page = requests.get(redi)
                redi_soup = BeautifulSoup(redi_page.content, "html.parser")
                club = redi_soup.find_all("td", class_="right")[1].text
                print(club)
                czasy.append(time.text)
                code = row.find("td", class_="code").text
                czasy.append(code)
                date = row.find("td", class_="date").text
                czasy.append(date)
                city = row.find("td", class_="city").text
                czasy.append(city)
                data_list.append(czasy)
df = pd.DataFrame(data_list)
print(df.head())
df.to_csv('athlete.csv')

