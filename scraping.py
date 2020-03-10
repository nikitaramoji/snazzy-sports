from crpapi import CRP
from bs4 import BeautifulSoup

import requests
import json

API_KEY = "8adcd451a0084c589292e7980a041d5c"

crp = CRP(API_KEY)
data = {}
company_names = ["Lockheed Martin", "Adobe Inc"]
missing_companies = []
cycle_years = ['2012', '2014', '2016', '2018']

years_to_name_to_id = {}
for year in cycle_years:
    f = open('{}_ids.json'.format(year), 'r')
    names_to_id = json.load(f)
    years_to_name_to_id[year] = names_to_id
    f.close()

for company_name in company_names:
    try:
        org = crp.fetch('getOrgs', org=company_name)
        org_id = org['organization']['@attributes']['orgid']
        data[company_name] = {}
        for year in cycle_years:
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

    except ValueError as e:
        print(e)
        print(company_name + " could not be found")
        missing_companies.append(company_name)

json_data = json.dumps(data)

print(data["Lockheed Martin"]['2012'])
