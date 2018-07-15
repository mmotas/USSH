from bs4 import BeautifulSoup as bs

from urllib.request import Request, urlopen
def openwebpage(url):
    #opener = urllib.build_opener()
    #opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    req = Request(url,headers={'User-Agent': 'Mozilla/5.0'})
    rp = urlopen(req)
    page = bs(rp, "html.parser")
    return page, rp.geturl()

fifa = {
    18:"",
    17:"fifa17_173/",
    16:"fifa16_73/",
    15:"fifa15_14/",
    14:"fifa14_13/",
    13:"fifa13_10/",
    12:"fifa12_9/",
    11:"fifa11_7/"
}

mls_fn = {
    18:"../../hackathon data/Hackathon Raw Files/Full Datasets - Opta/MLS/MLS 2017-2018.csv",
    17:"../../hackathon data/Hackathon Raw Files/Full Datasets - Opta/MLS/MLS 2016-2017.csv",
    16:"../../hackathon data/Hackathon Raw Files/Full Datasets - Opta/MLS/MLS 2016-2015.csv",
    15:"../../hackathon data/Hackathon Raw Files/Full Datasets - Opta/MLS/MLS 2015-2014.csv",
    14:"../../hackathon data/Hackathon Raw Files/Full Datasets - Opta/MLS/MLS 2014-2013.csv"
}

def get_player_page_url(page):
    table = page.find_all(attrs={"data-title":"Name"})
    a  = table[0].find('a')
    baseurl = "http://www.fifaindex.com"
    return baseurl+a['href']
    

def get_player_rating(page):
    span = page.find_all(attrs={"class":"label rating r3"})[0]
    return span.text.strip()
    

def get_player(player_name,year):
    base_url_start = "https://www.fifaindex.com/players/?name="
    base_url_end = "&order=desc"
    player_name = player_name.lower()
    player_name = player_name.encode("ascii", errors="ignore").decode()
    player_name = player_name.replace(" ","+")
    url = base_url_start+player_name+base_url_end
    try:
        page, rurl = openwebpage(url)
        print(url)
        second_url = get_player_page_url(page)+fifa[year]

        spage, rurl = openwebpage(second_url)
        if fifa[year] in rurl:
            return get_player_rating(spage), player_name.replace("+"," ")
        else:
            return -1, player_name.replace("+"," ")
    except Exception:
        return -1, player_name.replace("+"," ")
    

import pandas as pd

player_ratings = {}
no_data_players = []
year = 18
data = pd.read_csv(str(mls_fn[year]),encoding = "ISO-8859-1")
players = data['player']
players = list(set(players))



player_ratings = {}
no_data_players = []
fw = open(str(year)+".csv","w")
fq = open(str(year)+".txt","w")
c=0
for player in players:
    rating, player = get_player(str(player),year)
    if rating == -1:
        no_data_players.append(str(player))
        fw.write(player+"\n")
    else:
        player_ratings[player] = rating
        fw.write(player+","+rating+"\n")
    c+=1
    if c==5:
        fw.close()
        break

fw.close()