# Python 2 and 3:
from __future__ import print_function
from lxml import html
import requests
import urllib
import random
from math import floor
from multiprocessing.pool import ThreadPool
#Below is a suggested solution for memory issues
#def create_packs(n,lib):
 # while n:
   # n-=1
   # l = []
  #  l.extend(random.choice(lib["common"]) for i in range(10))
  #  l.extend(random.choice(lib["whatever"]) for i in range(3))
  #  if(random.random() < 0.125):
	#	pack[count] = mythics[floor(random.random() * len(mythics))]
#	else:
#	pack[count] = rares[floor(random.random() * len(rares))]
#yield l

def getRarity(rare, cards):
	cardlist = {}
	count = 0
	for ci in cards:
		if(cards[ci]["rarity"] == rare):
			cardlist[count] = cards[ci]
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

#function used to find average pack value
def average(numlist):
	count = 0
	value = 0
	for i in range(len(numlist)):
		value += numlist[count]
		count+=1
	return value/len(numlist)

#function used to find average box value, not used at this time due to runtime inefficency
def averageBox(numlist, totalBoxes, boxSize):
	count = 0
	value = 0
	for i in range(totalBoxes * boxSize):
		value += numlist[count]
		count += 1
	return value/totalBoxes

def boxCreation(boxCount, packCount):
	value = {}
	count = 0
	rare_values = {}
	for i in range(boxCount * packCount):
		pack = makePack(commons, uncommons, rares, mythics)
		rare_values[count] = pack[13]["value"]
		value[count] = getPackValue(pack)
		count+=1
	return value, rare_values
#start of program
setName = raw_input("Please input the acronym for the set (I.E Khans of Tarkir is KTK): ")
try:
	clist = getset(setName)
except:
	print("An error occured when getting the set, please check your acronym or try again later.")
	exit()

number_of_boxes = 1000
commons = getRarity("Common", clist)
uncommons = getRarity("Uncommon", clist)
rares = getRarity("Rare", clist)
mythics = getRarity("Mythic", clist)

pack_count = eval(raw_input("How many packs do you want to open: "))
value, rare_values = boxCreation(number_of_boxes, pack_count)
print("Set Name:{}".format(setName))
print("Total Average Pack Value: {}".format(average(value)))
print("Total Average Value of Rares/Mythics in a Pack: {}".format(average(rare_values)))
print("Total Average Box Value: {}".format(averageBox(value, number_of_boxes, pack_count)))
print("Total Average Value of Rares/Mythics in a Box: {}".format(averageBox(rare_values, number_of_boxes, pack_count)))