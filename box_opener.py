from lxml import html, etree
import requests
import urllib
import random
from math import floor
import math
from multiprocessing.pool import ThreadPool
import statistics

PACK_SIZE = 14  # Normal pack size without basic land or advertisement card
DEFAULT_BOX_SIZE = 36  # Number of packs per non-specialty set box
MYTHIC_RATE = 0.125  # Rough probability of opening a Mythic

def scrape_mtg_goldfish(set_acronym):
    page = requests.get('https://www.mtggoldfish.com/index/'+ set_acronym +'#paper')
    tree = html.fromstring(page.content)
    table = tree.xpath('//div[@class="index-price-table-paper"]/table/tbody/tr')
    cardlist = list()
    count = 0
    for row in table:
        columns = list(row)
        card = {
            'name': columns[0][0].text, # First element in scraped table is a hyperlink
            'rarity': columns[2].text or "Unknown",
            'value': float(columns[3].text)
        }
        cardlist.append(card)
    return cardlist

def get_cards_by_rarity(rarity, card_set):
    return list(filter(lambda card: card['rarity'] == rarity, card_set))

def generate_pack(card_set):
    pack = list()
    random.seed()
    commons = get_cards_by_rarity('Common', card_set)
    uncommons = get_cards_by_rarity('Uncommon', card_set)
    rares = get_cards_by_rarity('Rare', card_set)
    mythics = get_cards_by_rarity('Mythic', card_set)
    for i in range(PACK_SIZE):
        if(i < 10):
            pack.append(commons[floor(random.random() * len(commons))])
        elif(i < 13):
            pack.append(uncommons[floor(random.random() * len(uncommons))])
    if(random.random() < MYTHIC_RATE):
        pack.append(mythics[floor(random.random() * len(mythics))])
    else:
        pack.append(rares[floor(random.random() * len(rares))])
    return pack

def get_pack_value(pack):
    return sum(card['value'] for card in pack)

def open_box(card_set, total_packs):
    box = {
        "packs": list(),
        "total_value": 0,
        "rare_value": 0
    }
    for i in range(total_packs):
        pack = generate_pack(card_set)
        box['packs'].append(pack)
        box["total_value"] += get_pack_value(pack)
        box["rare_value"] += pack[-1]["value"]
    return box

def thread_handler(number_of_boxes, total_packs, card_set):
    print("child process running...")
    boxes = list()
    for i in range(int(number_of_boxes)):
        boxes.append(open_box(card_set, total_packs))
    return boxes


# Start of script
set_acronym = input("Please input the acronym for the set (I.E Khans of Tarkir is KTK): ")
try:
	card_set = scrape_mtg_goldfish(set_acronym)
except:
	print("An error occured when getting the set, you are doing too many queries or disconnected from the internet, try again later")
	exit()
if(len(card_set) == 0):
	print("An error occured. Set is empty. Check if your acronym is correct")
	exit()

pack_count = eval(input("Number of packs being opened: "))

number_of_boxes = 16000
print("Cracking open boxes")
pool = ThreadPool(processes = 8)
async_result1 = pool.apply_async(thread_handler, (number_of_boxes/8, pack_count, card_set))
async_result2 = pool.apply_async(thread_handler, (number_of_boxes/8, pack_count, card_set))
async_result3 = pool.apply_async(thread_handler, (number_of_boxes/8, pack_count, card_set))
async_result4 = pool.apply_async(thread_handler, (number_of_boxes/8, pack_count, card_set))
async_result5 = pool.apply_async(thread_handler, (number_of_boxes/8, pack_count, card_set))
async_result6 = pool.apply_async(thread_handler, (number_of_boxes/8, pack_count, card_set))
async_result7 = pool.apply_async(thread_handler, (number_of_boxes/8, pack_count, card_set))
async_result8 = pool.apply_async(thread_handler, (number_of_boxes/8, pack_count, card_set))
boxes1 = async_result1.get()
boxes2 = async_result2.get()
boxes3 = async_result3.get()
boxes4 = async_result4.get()
boxes5 = async_result5.get()
boxes6 = async_result6.get()
boxes7 = async_result7.get()
boxes8 = async_result8.get()

boxes = boxes1 + boxes2 + boxes3 + boxes4 + boxes5 + boxes6 + boxes7 + boxes8
# Box statistics
print("Average value of a box: {}".format(statistics.mean(box['total_value'] for box in boxes)))
print("Average value of rares/mythics in a box: {}".format(statistics.mean(box['rare_value'] for box in boxes)))
print("Median value of a box: {}".format(statistics.median(box['total_value'] for box in boxes)))
print("Median value of a rares/mythics in a box: {}".format(statistics.median(box['rare_value'] for box in boxes)))

# Pack statistics
