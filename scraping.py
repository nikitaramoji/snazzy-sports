from bs4 import BeautifulSoup

import requests
import json
import csv
import random


data = {}
with open('/Users/sbarshay/Downloads/Value Errors - Sheet1.csv', newline='') as f:
    reader = csv.reader(f)
    companies = list(reader)
missing_companies = []
cycle_years = ['2012', '2014', '2016''2018']
type_error_companies = []

years_to_name_to_id = {}
for year in cycle_years:
    f = open('{}_ids.json'.format(year), 'r')
    names_to_id = json.load(f)
    years_to_name_to_id[year] = names_to_id
    f.close()
i = 1
for company in companies:
    print(i)
    i += 1
    try:
        company_name = company[0]
        org_id = company[1]
        data[company_name] = {}
        for year in cycle_years:
            try:
                data[company_name][year] = []
                cycle_url = "https://www.opensecrets.org/orgs/recipients?toprecipscycle=" + year + "&candscycle=2020&id=" + org_id + "&t3-Type=Cand"
                response = requests.get(cycle_url)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                full_candidate_info_table = soup.find(id="top_recipients-inner-container").find("table").find("tbody").find_all("tr")
                for candidate_info in full_candidate_info_table:
                    indiv_info = candidate_info.find_all("td")
                    demographic_info = indiv_info[4].text.split(" ")
                    if demographic_info[0] == 'Candidate':
                        name = indiv_info[0].text
                        total_amount = float(indiv_info[1].text[1:].replace(',','').strip('$'))
                        party = demographic_info[0][1]
                        election_type = demographic_info[0][3:-1]
                        if(len(name) > 1):
                            data[company_name][year].append((name, total_amount, party, election_type))
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
f = open("data5","w")
f.write(json_data)
f.close()
