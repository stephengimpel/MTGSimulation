# Python 2 and 3:
from __future__ import print_function
from lxml import html
import requests
import urllib
import random
from math import floor
from multiprocessing.pool import ThreadPool
import time
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

def merge_dicts(x, y, a, b):
    z = x.copy()
    z.update(y)
    z.update(a)
    z.update(b)
    return z

def boxCreation(boxCount, packCount, pnum, start):
	print("Process {}".format(pnum))
	value = {}
	count = start * packCount
	rare_values = {}
	for i in range(boxCount * packCount):
		pack = makePack(commons, uncommons, rares, mythics)
		rare_values[count] = pack[13]["value"]
		value[count] = getPackValue(pack)
		count+=1
	return value, rare_values

#start of program
start_time = time.time()
setName = raw_input("Please input the acronym for the set (I.E Khans of Tarkir is KTK): ")
try:
	clist = getset(setName)
except:
	print("An error occured when getting the set, you are doing too many queries, try again later")
	exit()
if(clist == {}):
	print("An error occured. Set is empty. Check if your acronym is correct")
	exit()
number_of_boxes = 1000
commons = getRarity("Common", clist)
uncommons = getRarity("Uncommon", clist)
rares = getRarity("Rare", clist)
mythics = getRarity("Mythic", clist)

pack_count = eval(raw_input("How many packs do you want to open: "))
pool = ThreadPool(processes=4)
print("Running simulation, this will take awhile")
async_result1 = pool.apply_async(boxCreation, (number_of_boxes/4, pack_count, 1, 0))
async_result2 = pool.apply_async(boxCreation, (number_of_boxes/4, pack_count, 2, number_of_boxes/4))
async_result3 = pool.apply_async(boxCreation, (number_of_boxes/4, pack_count, 3, number_of_boxes/2))
async_result4 = pool.apply_async(boxCreation, (number_of_boxes/4, pack_count, 4, (3*number_of_boxes)/4))
#value, rare_values = boxCreation(number_of_boxes/2, pack_count, 1)
tvalue1, trare1 = async_result1.get()
tvalue2, trare2 = async_result2.get()
tvalue3, trare3 = async_result3.get()
tvalue4, trare4 = async_result4.get()
value = merge_dicts(tvalue1,tvalue2,tvalue3,tvalue4)
rare_values = merge_dicts(trare1,trare2,trare3,trare4)
print("Set Name:{}".format(setName))
print("Total Average Pack Value: {}".format(average(value)))
print("Total Average Value of Rares/Mythics in a Pack: {}".format(average(rare_values)))
print("Total Average Box Value: {}".format(averageBox(value, number_of_boxes, pack_count)))
print("Total Average Value of Rares/Mythics in a Box: {}".format(averageBox(rare_values, number_of_boxes, pack_count)))
print("--- %s seconds ---" % (time.time() - start_time))