from urllib.request import *
from bs4 import *
import urllib
from collections import defaultdict
from pandas import Series, DataFrame

baseUrlTeamDef = "http://www.statiz.co.kr/stat.php?opt=0&sopt=0&re=1&ys={}&ye={}&se=0&te=&tm=&ty=0&qu=auto&po=0&as=&ae=&hi=&un=&pl=&da=1&o1=WAR&o2=OutCount&de=1&lr=5&tr=&cv=&ml=1&sn=30&si=&cn="
baseUrlTeamAtt = "http://www.statiz.co.kr/stat.php?opt=0&sopt=0&re=0&ys={}&ye={}&se=0&te=&tm=&ty=0&qu=auto&po=0&as=&ae=&hi=&un=&pl=&da=1&o1=WAR_ALL_ADJ&o2=TPA&de=1&lr=5&tr=&cv=&ml=1&sn=30&si=&cn="
baseUrlPay = "http://www.statiz.co.kr/team.php?cteam={}&year={}&opt=0&sopt=8"

dataAtt = dict(LG = [], KIA = [], 해태 = [], SSG = [], NC = [], 삼성 = [], KT = [], 두산 = [], OB = [], 롯데 = [], 한화 = [], 히어로즈 = [], 넥센 = [], 키움 = [], SK = [], 쌍방울 = [], MBC = [], 현대 = [])
dataDef = dict(LG = [], KIA = [], 해태 = [], SSG = [], NC = [], 삼성 = [], KT = [], 두산 = [], OB = [], 롯데 = [], 한화 = [], 히어로즈 = [], 넥센 = [], 키움 = [], SK = [], 쌍방울 = [], MBC = [], 현대 = [])

years = range(2013, 2023)


#attack
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

indexatt = []
valueatt = []
for team, dictval in dataAtt.items():
    for obj in dictval:
        indexatt.append(team+str(obj[0]))
        valueatt.append(obj[1])

attS = Series(valueatt, index = indexatt)

#defence
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

indexdef = []
valuedef = []
for team, dictval in dataDef.items():
    for obj in dictval:
        indexdef.append(team+str(obj[0]))
        valuedef.append(obj[1])

defS = Series(valuedef, index = indexdef)

totalS = attS + defS

for team, dictval in dataDef.items():
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

indexpay = []
valuepay = []
for team, dictval in dataDef.items():
    for obj in dictval:
        indexpay.append(team+str(obj[0]))
        valuepay.append(obj[2])

payS = Series(valuepay, index = indexpay)

DF = DataFrame({'teamyear': attS.index, 'attwar': attS.values, 'defwar': defS.values, 'totalwar': totalS.values, 'pay': payS.values})

DF.to_csv("warandpay.csv", mode='w', encoding='utf-8-sig')
