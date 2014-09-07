from bs4 import BeautifulSoup
import urllib2
import datetime
import decimal

#given a table of playoff totals, return the average age of the team, scaled per minutes played
def getAvgAge(table):
    rows = table.findAll('tr')
    minuteTotal = 0
    ageTotal = 0
    for i in range(1, len(rows)):
        row = rows[i]
        td = row.findAll('td')
        #ageTotal becomes the numerator in the WAGE equation
        ageTotal = ageTotal + float(td[2].text) * float(td[5].text)
        #minuteTotal becomes the denominator in the WAGE equation
        minuteTotal = minuteTotal + float(td[5].text)
    return ageTotal/minuteTotal

ABA = 'ABA'
currYear = datetime.datetime.now().year
#start in 1952 because before that, playoff minutes weren't recorded
firstYear = 1952
numYears = currYear - firstYear + 1

baseurl1 = "http://www.basketball-reference.com/leagues/BAA_"
baseurl2 = "http://www.basketball-reference.com/leagues/NBA_"
base = "http://www.basketball-reference.com"

teamURLs = [""] * numYears
champs   = [""] * numYears

url = base + "/leagues"
soup = BeautifulSoup(urllib2.urlopen(url))

tblSeasons = soup.find('table')
rows = tblSeasons.findAll('tr')

i = 0
rowNum = 3
while(i <= (currYear - firstYear)):
    currRow = rows[rowNum]
    #find all NBA championship team URLs, exclude ABA
    if(currRow.findAll('td')[1].a.text != ABA):
        teamURLs[i] = currRow.findAll('td')[2].a['href']
        i = i + 1
    rowNum = rowNum + 1

i = 0
for extension in teamURLs:
    url = base + extension
    #opens the page for one NBA championship team
    soup = BeautifulSoup(urllib2.urlopen(url))
    tblPlayoffs = soup.find(id="playoffs_totals")
    #tuple 1 gets grabs the name of the team as a string
    age = getAvgAge(tblPlayoffs)
    champs[i] = (soup.h1.text.split(" Roster")[0], str(format(age, '.3f')))
    i = i + 1

champs = sorted(champs, key=lambda tup: tup[1])
for champ in champs:
    print champ[0] + "," + champ[1]
