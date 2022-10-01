from urllib.request import *
from bs4 import *
import urllib
from collections import defaultdict
baseUrlTeam = "http://www.statiz.co.kr/stat.php?opt=0&sopt=0&re=0&ys={}&ye={}&se=0&te=&tm=&ty=0&qu=auto&po=0&as=&ae=&hi=&un=&pl=&da=1&o1=WAR_ALL_ADJ&o2=TPA&de=1&lr=5&tr=&cv=&ml=1&sn=30&si=&cn="
baseUrlPay = "http://www.statiz.co.kr/team.php?cteam={}&year={}&opt=0&sopt=8"

data = dict(LG = [], KIA = [], 해태 = [], SSG = [], NC = [], 삼성 = [], KT = [], 두산 = [], OB = [], 롯데 = [], 한화 = [], 히어로즈 = [], 넥센 = [], 키움 = [], SK = [], 쌍방울 = [], MBC = [], 현대 = [])
year_max_data = defaultdict(list)
year_min_data = defaultdict(list)
my_team = defaultdict(list)

years = range(2013, 2023)

print("Input Your favorite TeamName : ",end = "")
my_team_name = input()

for year in years:
    #print(baseUrlTeam.format(year, year))
    req = Request(baseUrlTeam.format(year, year))
    wp = urlopen(req)
    soup = BeautifulSoup(wp, 'html.parser')
    tableRaw = soup.find("table", id="mytable").find_all('tr')
    trList = tableRaw[7:]
    for tr in trList:
        tdList = tr.find_all('td')
        teamname = tdList[1].get_text().upper()
        warvalue = tdList[3].find('span').get_text()
        data[teamname].append([year, float(warvalue)])
        #print(data[teamname])

#print(data)

for team, dictval in data.items():
    for obj in dictval:
        #print(baseUrlPay.format(team, obj[0]))
        year = obj[0]
        req = Request(baseUrlPay.format(urllib.parse.quote(team), year))
        wp = urlopen(req)
        soup = BeautifulSoup(wp, 'html.parser')
        trList = soup.find("table", "table table-striped").find_all('tr')
        #print(trList)
        trList.pop(0)
        totalpay = 0
        
        for tr in trList:
            tdList = tr.find_all('td')
            temp = int(tdList[1].get_text().replace(',', ''))
            totalpay += temp

        obj.append(totalpay)
        #print(totalpay)

for team, year_arr in data.items():
    if team == '키움':
        continue
    for year, war, price in year_arr:
        eff = price / war

        if len(year_max_data[year])==0:
            year_max_data[year].append([eff,team])
        elif year_max_data[year][0][0] < eff:
            year_max_data[year][0][0] = eff
            year_max_data[year][0][1] = team

        if len(year_min_data[year])==0:
            year_min_data[year].append([eff,team])
        elif year_min_data[year][0][0] > eff:
            year_min_data[year][0][0] = eff
            year_min_data[year][0][1] = team

        if team == my_team_name:
            my_team[year].append([eff,team])
        
print(year_max_data)
print(year_min_data)
print(my_team)
