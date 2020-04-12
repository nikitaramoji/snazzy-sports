from crpapi import CRP
from bs4 import BeautifulSoup

import requests
import json
import csv

API_KEY = "21c4b2ad2e76b2e7d6524a9bccbf5119"

crp = CRP(API_KEY)
data = {}
with open('/Users/danielkotroco/github/snazzy-sports/Value-Errors-Sheet1.csv', newline='') as f:
    reader = csv.reader(f)
    companies = list(reader)
missing_companies = []
cycle_years = ['2012','2014', '2016', '2018']
type_error_companies = []

years_to_name_to_id = {}
for year in cycle_years:
    f = open('{}_ids.json'.format(year), 'r')
    names_to_id = json.load(f)
    years_to_name_to_id[year] = names_to_id
    f.close()

for company in companies:
    try:
        company_name = company[0]
        org_id = company[1]
        data[company_name] = {}
        for year in cycle_years:
            try:
                data[company_name][year] = []
                cycle_url = "https://www.opensecrets.org/orgs/recips.php?cycle=" + year + "&id=" + org_id
                response = requests.get(cycle_url)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                full_candidate_info_table = soup.find(id="recips").find("tbody").find_all("tr")
                for candidate_info in full_candidate_info_table:
                        name = candidate_info.find_all("td")[0].text.split(" ")
                        # print(year, name)
                        # cid = years_to_name_to_id[year][name[0] + ' ' + name[1]]
                        data[company_name][year].append(str(name[1] + " " + name[0][:-1]))
            except AttributeError as e:
                print(e)
                print(company_name + " could not be found (AttributeError)" + year)
    except ValueError as e:
        print(e)
        print(company_name + " could not be found (ValueError)")
        missing_companies.append(company_name)
    except TypeError as e:
        print(e)
        print(company_name + " could not be found (TypeError)")
        type_error_companies.append(company_name)

json_data = json.dumps(data)

print(missing_companies)
print(len(missing_companies))
print(type_error_companies)
print(len(type_error_companies))
f = open("company_opensecrets_dataFINAL","w")
f.write(json_data)
f.close()
