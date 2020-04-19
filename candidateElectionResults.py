from crpapi import CRP
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError
import time
import requests
import json

API_KEY = "8adcd451a0084c589292e7980a041d5c"

crp = CRP(API_KEY)
data = {}
missing_cids = []
cycle_years = ['2012', '2014', '2016', '2018']
# create sets of winners for each election cycle to check for membership
setWinners = {'2012' : set(), '2014': set(), '2016': set(), '2018': set()}

# 2012 - N00009638 : win
# 2012 - N00000286 : loss (haha)
# 2016 - N00023864 : win :,(
# 2016 - N00000019 : loss >:(

file = open("ElectionResults.csv", 'r')
line = file.readline()
line = file.readline()

years_to_ids_to_win = {}

while line:
    members = line.split(",")
    setWinners['2012'].add(members[0])
    setWinners['2014'].add(members[1])
    setWinners['2016'].add(members[2])
    line = file.readline()



years_to_name_to_id = {}
for i in range(len(cycle_years) - 1):
    count = 0
    year = cycle_years[i]
    f = open('{}_ids.json'.format(year), 'r')
    names_to_id = json.load(f)
    #print(names_to_id)
    #years_to_name_to_id[year] = names_to_id
    years_to_ids_to_win[year] = {}
    f.close()
    for name_id_pair in names_to_id.items():
        id = name_id_pair[1]
        #print(name_id_pair)
        years_to_ids_to_win[year][id] = {}
        if id in setWinners[year] and id != "NaN":
            years_to_ids_to_win[year][id] = 1
        else:
            years_to_ids_to_win[year][id] = 0

from itertools import islice

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

years_to_ids_to_win['2018'] = {}

f = open('{}_ids.json'.format('2018'), 'r')
names_to_id = json.load(f)
count = 0

# for name_id_pair in names_to_id.items():
#     curr_id = name_id_pair[1]
#
#     cycle_url = 'https://www.opensecrets.org/members-of-congress/summary?cid=' + curr_id
#     try:
#         response = requests.get(cycle_url)
#         response.raise_for_status()
#         if "Please go back or try a new search." in response.text:
#             #print(response.text)
#             #print("Oy")
#             years_to_ids_to_win['2018'][curr_id] = 0
#         else:
#             count = count + 1
#             years_to_ids_to_win['2018'][curr_id] = 1
#             #print(name_id_pair[0])
#         #print(response.content)
#
#     except HTTPError as e:
#         #print(curr_id)
#         years_to_ids_to_win['2018'][curr_id] = 0
# print(count)
# print(years_to_ids_to_win)
json_data = json.dumps(years_to_ids_to_win)
f = open("election_winner.json","w")
f.write(json_data)
f.close()
