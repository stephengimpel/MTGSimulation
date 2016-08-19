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
	page = requests.get('https://www.mtggoldfish.com/index/'+name +'#paper')
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

def average(cardlist):
	count = 0
	value = 0
	while count < len(cardlist):
		value += cardlist[count]
		count+=1
	return value/len(cardlist)
#main();
#start of program
setName = raw_input("Please input the acronym for the set (I.E Khans of Tarkir is KTK): ")
clist = getset(setName)
if(clist == {}):
	print("An error occured when getting the set, please check your acronym or try again later.")
	exit()
commons = getRarity("Common", clist)
uncommons = getRarity("Uncommon", clist)
rares = getRarity("Rare", clist)
mythics = getRarity("Mythic", clist)
value = {}
scount = 0
pcount = 0
vcount = 0
rare_values = {}
pack_count = eval(raw_input("How many packs are in this box: "))
while(scount < 10000):
	while(pcount < pack_count):
		pack = makePack(commons, uncommons, rares, mythics)
		rare_values[vcount] = pack[13]["value"]
		value[vcount] = getPackValue(pack)
		pcount += 1
		vcount +=1
	scount+=1
	pcount=0
print(value)
print("Set Name:{}".format(setName))
print("Total Average Box Value: {}".format(average(value)))
print("Total Average Value of Rares in a Box: {}".format(average(rare_values)))