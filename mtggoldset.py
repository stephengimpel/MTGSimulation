# Python 2 and 3:
from __future__ import print_function
from lxml import html
import requests
import urllib
def main():
	page = requests.get('http://econpy.pythonanywhere.com/ex/001.html');
	tree = html.fromstring(page.content);
	#This will create a list of buyers:
	buyers = tree.xpath('//div[@title="buyer-name"]/text()');
	#This will create a list of prices
	prices = tree.xpath('//span[@class="item-price"]/text()');
	print("Buyers: ", buyers);
	print("Prices: ", prices);

def getset(name):
	#page = requests.get('https://www.mtggoldfish.com/index/'+name +'#paper');
	page = open("scrape.html").read()
	tree = html.fromstring(page);
	#/html/body/div[2]/div[7]/div[2]/table/tbody
	cards = tree.xpath('//div[@class="index-price-table-paper"]/table/tbody/tr')
	#tree.cssselect('.index-price-table-online [aria-live=polite]')
	#map = func applied to each index in an iterable
	#fliter = each element is given an arugmenet to the function filter, and the function
	#returns t or f. T = included in return F = no way jose. Removes empty strings
	#cards = map(str.strip,cards)
	cardlist = {}
	#print(cards)
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
		cardlist[name] = cd
	#print("{} is {} and valued at ${:.2}".format(name,rarity,value))
	#names = tree.xpath('//td[@class="card"]/a/text()');
	#price = tree.xpath('//tr/td[@class="text-right"][1]/text()');
	#price = filter(len,map(str.strip,price))
	#rarity = tree.xpath('//tr/td[3]/text()')
	#rarity = filter(len, map(str.strip,rarity))
	#test = map(float,[t[:-1] for t in test])
	#for p in prices:
	#	print(html.tostring(p))
	#print(names);
	#print(rarity)
	#print(name);
	print(cardlist)
#main();
getset("SOI")