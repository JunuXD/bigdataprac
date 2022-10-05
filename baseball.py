from urllib.request import *
from bs4 import *
import urllib
from collections import defaultdict
import matplotlib.pyplot as p

baseUrlTeamDef = "http://www.statiz.co.kr/stat.php?opt=0&sopt=0&re=1&ys={}&ye={}&se=0&te=&tm=&ty=0&qu=auto&po=0&as=&ae=&hi=&un=&pl=&da=1&o1=WAR&o2=OutCount&de=1&lr=5&tr=&cv=&ml=1&sn=30&si=&cn="
baseUrlTeamAtt = "http://www.statiz.co.kr/stat.php?opt=0&sopt=0&re=0&ys={}&ye={}&se=0&te=&tm=&ty=0&qu=auto&po=0&as=&ae=&hi=&un=&pl=&da=1&o1=WAR_ALL_ADJ&o2=TPA&de=1&lr=5&tr=&cv=&ml=1&sn=30&si=&cn="
baseUrlPay = "http://www.statiz.co.kr/team.php?cteam={}&year={}&opt=0&sopt=8"

dataAtt = dict(LG = [], KIA = [], SSG = [], NC = [], 삼성 = [], KT = [], 두산 = [], 롯데 = [], 한화 = [], 넥센 = [], 키움 = [], SK = [])
dataDef = dict(LG = [], KIA = [], SSG = [], NC = [], 삼성 = [], KT = [], 두산 = [], 롯데 = [], 한화 = [], 넥센 = [], 키움 = [], SK = [])
dataTot = dict(LG = [], KIA = [], SSG = [], NC = [], 삼성 = [], KT = [], 두산 = [], 롯데 = [], 한화 = [], 넥센 = [], 키움 = [], SK = [])

max_data = defaultdict(float)
min_data = defaultdict(float)
my_data = defaultdict(float)

years = range(2013, 2023)


#UI - Input TeamName -> graph
print("Team Efficiency Information(LG, KIA, SSG, NC, 삼성, KT, 두산, 롯데, 한화, 넥센, SK)")
print("Input Your favorite TeamName : ",end = "")
my_team_name = input()


# Change Team Name to English
def check_name(name):
    if name == '한화':
        return 'HANHWA'
    elif name == '넥센':
        return 'NEXEN'
    elif name == '삼성':
        return 'SAMSUNG'
    elif name == '두산':
        return 'DOOSAN'
    elif name == '롯데':
        return 'LOTTE'
    else:
        return name

#Draw Efficiency Graph
def drawGraph():
    xAxis = list(range(2013,2023))
    myAxis = list(my_data.keys())
    
    highList = list(max_data.values())
    lowList = list(min_data.values())
    myList = list(my_data.values())

    name = check_name(my_team_name)

    p.xticks(range(2013,2023))
    p.plot (xAxis, highList,    'ro-', label = 'high')
    p.plot (xAxis, lowList,  'b^-', label = 'low')     
    p.plot (myAxis, myList, 'gx-', label = name)    
    
    p.xlabel ('Year')
    p.ylabel ('Team Efficiency')
    p.grid (True)
    p.legend(loc = 'upper left')
    p.show()


#Crawl Attack Information
for year in years:
    req = Request(baseUrlTeamAtt.format(year, year))
    wp = urlopen(req)
    soup = BeautifulSoup(wp, 'html.parser')
    tableRaw = soup.find("table", id="mytable").find_all('tr')
    trList = tableRaw[7:]
    for tr in trList:
        tdList = tr.find_all('td')
        teamname = tdList[1].get_text().upper()
        warvalue = tdList[3].find('span').get_text()
        dataAtt[teamname].append([year, float(warvalue)])

#Crawl Defense Information
for year in years:
    req = Request(baseUrlTeamDef.format(year, year))
    wp = urlopen(req)
    soup = BeautifulSoup(wp, 'html.parser')
    tableRaw = soup.find("table", id="mytable").find_all('tr')
    trList = tableRaw[7:]
    for tr in trList:
        tdList = tr.find_all('td')
        teamname = tdList[1].get_text().upper()
        warvalue = tdList[3].find('span').get_text()
        dataDef[teamname].append([year, float(warvalue)])

#Crawl Pay Information
for team, dictval in dataDef.items():
    for obj in dictval:
        year = obj[0]
        req = Request(baseUrlPay.format(urllib.parse.quote(team), year))
        wp = urlopen(req)
        soup = BeautifulSoup(wp, 'html.parser')
        trList = soup.find("table", "table table-striped").find_all('tr')
        trList.pop(0)
        totalpay = 0
        
        for tr in trList:
            tdList = tr.find_all('td')
            temp = int(tdList[1].get_text().replace(',', ''))
            totalpay += temp

        obj.append(totalpay)


#Data Processing(Attack WAR + Defence WAR)
for Def, Att in zip(dataDef.items(), dataAtt.items()):
    for d_info,a_info in zip(Def[1],Att[1]):
        dataTot[Def[0]].append([d_info[0], d_info[1]+a_info[1], d_info[2]])


#Data Processing(Pay / Total WAR) and Store myTeamName Information
for team, year_arr in dataTot.items():
    if team == '키움': #키움 has no information about pay
        continue
    
    for year, war, price in year_arr:
        eff = price / war

        max_data[year] = max(max_data[year], eff)
        if min_data[year] == 0:
            min_data[year] = eff
        else:
            min_data[year] = min(min_data[year], eff)

        if team == my_team_name:
            my_data[year] = eff


drawGraph()
