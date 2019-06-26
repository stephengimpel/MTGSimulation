# Python 2 and 3:
from __future__ import print_function
from lxml import html
import requests
import urllib
import random
from math import floor
import math
from multiprocessing.pool import ThreadPool
import time
import statistics
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

#function used to find average box value, not used at this time due to runtime inefficency
def averageBox(numlist, totalBoxes):
	return sum(numlist)/totalBoxes

def boxCreation(boxCount, packCount, pnum):
	print("Process {}".format(pnum))
	value = []
	rare_values = []
	for i in range(int(boxCount * packCount)):
		pack = makePack(commons, uncommons, rares, mythics)
		rare_values.append(pack[13]["value"])
		value.append(getPackValue(pack))
	return value, rare_values#, pmax, pmin, rmin

#start of program
start_time = time.time()
setName = input("Please input the acronym for the set (I.E Khans of Tarkir is KTK): ")
try:
	clist = getset(setName)
except:
	print("An error occured when getting the set, you are doing too many queries or disconnected from the internet, try again later")
	exit()
if(clist == {}):
	print("An error occured. Set is empty. Check if your acronym is correct")
	exit()

commons = getRarity("Common", clist)
uncommons = getRarity("Uncommon", clist)
rares = getRarity("Rare", clist)
mythics = getRarity("Mythic", clist)

pack_count = eval(input("How many packs do you want to open: "))
print("How accurate do you want your information?(This relies heavily on processor speed!)")
print("1. Minimum (1,000 trials)")
print("2. Adequate (10,000 trials")
user = eval(input("3. Thorough (100,000 trials)\n"))
number_of_boxes = 0
if(user == 1):
	number_of_boxes = 1000
elif(user == 2):
	number_of_boxes = 10000
elif(user == 3):
	number_of_boxes = 100000
else:
	print("You did not select a proper input, using minimum.")
	number_of_boxes = 1000
pool = ThreadPool(processes=8)
print("Running simulation, this will take awhile")
async_result1 = pool.apply_async(boxCreation, (number_of_boxes/8, pack_count, 1))
async_result2 = pool.apply_async(boxCreation, (number_of_boxes/8, pack_count, 2))
async_result3 = pool.apply_async(boxCreation, (number_of_boxes/8, pack_count, 3))
async_result4 = pool.apply_async(boxCreation, (number_of_boxes/8, pack_count, 4))
async_result5 = pool.apply_async(boxCreation, (number_of_boxes/8, pack_count, 5))
async_result6 = pool.apply_async(boxCreation, (number_of_boxes/8, pack_count, 6))
async_result7 = pool.apply_async(boxCreation, (number_of_boxes/8, pack_count, 7))
async_result8 = pool.apply_async(boxCreation, (number_of_boxes/8, pack_count, 8))
tvalue1, trare1 = async_result1.get()
tvalue2, trare2 = async_result2.get()
tvalue3, trare3 = async_result3.get()
tvalue4, trare4 = async_result4.get()
tvalue5, trare5 = async_result5.get()
tvalue6, trare6 = async_result6.get()
tvalue7, trare7 = async_result7.get()
tvalue8, trare8 = async_result8.get()
pool.close()
pool.join()
value = tvalue1+tvalue2+tvalue3+tvalue4+tvalue5+tvalue6+tvalue7+tvalue8
rare_values = trare1+trare2+trare3+trare4+trare5+trare6+trare7+trare8
#zasync_result2 = pool.apply_async(average, rare_values)
avgrare = statistics.mean(rare_values)
avgv = statistics.mean(value)
avgb = averageBox(value, number_of_boxes)
avgrb = averageBox(rare_values, number_of_boxes)
print("Set Name:{}".format(setName))
print("Total Average Pack Value: {}".format(avgv))
print("Total Average Value of Rares/Mythics in a Pack: {}".format(avgrare))
print("Total Average Box Value: {}".format(avgb))
print("Total Average Value of Rares/Mythics in a Box: {}".format(avgrb))
print("Box Median: {}".format(statistics.median(value)));
print("Rare Median: {}".format(statistics.median(rare_values)));
print("Standard Deviation for packs: {}".format(statistics.stdev(value)))
print("Standard Deviation for Rares/Mythics in a pack: {}".format(statistics.stdev(rare_values)))
print("Median pack value: {}".format(statistics.median(value)))
print("Median Rare/Mythics in a pack: {}".format(statistics.median(rare_values)))
print("Variance of pack value: {}".format(statistics.variance(value)))
print("Variance of Rare/Mythics in a pack: {}".format(statistics.variance(rare_values)))
print("Most valuable card in the set(Max Price on Card): {}".format(list(clist.values())[0]))
print("Least valuable card in the set(Min Price on Card): {}".format(list(clist.values())[len(clist)-1]))
print("--- %s seconds ---" % (time.time() - start_time))
