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

def pricer(name):
	name = urllib.urlencode({"q":name, "v":"card", "s":"cname"})
	page = requests.get('http://magiccards.info/query?'+name);
	tree = html.fromstring(page.content);
	prices = tree.xpath('//td');
	for p in prices:
		print(html.tostring(p))
	print(prices);
	print(name);
#main();
pricer("Goblin Guide")