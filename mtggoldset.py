# Python 2 and 3:
from __future__ import print_function
from lxml import html
import requests
import urllib
import random
from math import floor
def getRarity(rare, cards):
	cardlist = {}
	count = 0
	for ci in cards:
		#print(cards[ci]["rarity"])
		if(cards[ci]["rarity"] == rare):
			cardlist[count] = cards[ci]
			#print(cardlist[count])
			count += 1
	
	return cardlist

def makePack(commons, uncommons, rares, mythics):
	pack = {}
	random.seed()
	count = 0
	while(count < 10):
		pack[count] = commons[floor(random.random() * len(commons))]
		count += 1
	while(count < 13):
		pack[count] = uncommons[floor(random.random() * len(uncommons))]
		count += 1
	if(random.random() < 0.125):
		pack[count] = mythics[floor(random.random() * len(mythics))]
	else:
		pack[count] = rares[floor(random.random() * len(rares))]
	return pack

def getPackValue(pack):
	num = 0
	for i in pack:
		num += pack[i]["value"]
	return num

def getset(name):
	page = requests.get('https://www.mtggoldfish.com/index/'+name +'#paper');
	#page = open("scrape.html").read()
	tree = html.fromstring(page.content);
	cards = tree.xpath('//div[@class="index-price-table-paper"]/table/tbody/tr')
	cardlist = {}
	count = 0
	for i,ci in enumerate(cards):
		data = list(ci)
		di = data[0].iter()
		next(di)
		name = next(di).text
		rarity = data[2].text or "Unknown Rarity"
		value = float(data[3].text)
		cd = {
			"name":name,
			"rarity":rarity,
			"value":value
		}
		cardlist[count] = cd
		count +=1
	return cardlist
#main();
#start of program
clist = getset("EMN")
commons = getRarity("Common", clist)
uncommons = getRarity("Uncommon", clist)
rares = getRarity("Rare", clist)
mythics = getRarity("Mythic", clist)
value = 0
scount = 0
pcount = 0
rare_values = 0
while(scount < 10000):
	while(pcount < 36):
		pack = makePack(commons, uncommons, rares, mythics)
		rare_values += pack[13]["value"]
		value += getPackValue(pack)
		pcount += 1
	scount+=1
	pcount=0
print(value/10000)
print(rare_values/10000)