# -*- coding: utf-8 -*-

import requests, os, time
from bs4 import BeautifulSoup



############ Scraping script
# This script aims at collecting team rosters for a given year
# 
# Process:
#    1. connect to main website
#    2. get links for every team, connect
#    3. get rosters
#    4. save info in txt file
#################################################################################


path = 'C:/Users/Thibault/Desktop/MVA/Graph/Project/Material/Tables/' # a changer
outputfile = path + 'rosters_scraped.txt'
f = open(outputfile, 'w', encoding='utf-8')
season = '2009' #season wanted

#we get data from fow news website
teams_url = 'http://www.foxsports.com/college-basketball/teams'
r = requests.get(teams_url)
html = r.text
soup = BeautifulSoup(html)

#parse to get list of teams links
team = soup.find_all('a', class_="team-index-block-item-img-container")
i = 0

#loop on teams
for link in team:
    i += 1
    line  = []
    
    a = str(link).split(' ')[2].replace('href="','').replace('">','').replace('\n','').replace('<img','')

    #connect to team roster page
    url = 'http://www.foxsports.com'+a+'-roster?season='+season
    team_clean = a.replace('/college-basketball/','').replace('-team','').replace('-',' ')
    rteam = requests.get(url)

    #parse webpage
    html2 = rteam.text
    soup2 = BeautifulSoup(html2)
    player = soup2.find_all('td', class_="wisfb_text")
    names = BeautifulSoup(str(BeautifulSoup(str(player)).find_all('span'))).text

    #clean
    namescl = names.replace('[', '').replace(']', '').split(', ')

    #format + write in output file
    for nom, prenom in zip(namescl[0::2], namescl[1::2]):
        ligne = team_clean + ',' + season + ',' + str(nom) + ',' + str(prenom) + '\r\n'
        f.write(ligne)
    print(i, team_clean)
f.close()    
