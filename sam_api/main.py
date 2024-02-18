import requests
import os
import json
import datetime

def init_search_terms(limit=10, posted_from="01/01/2024",
                      posted_to=None, ptype=None, ncode=None):
    api_key = os.getenv('SAM_API_KEY')
    print(api_key)
    if not api_key:
        print("Valid API Key not found")
        exit(-1)
    
    if not posted_to:
        posted_to = datetime.date.today().strftime("%m/%d/%y") 

    terms = {}
    terms['limit'] = limit
    terms['postedFrom'] = posted_from
    terms['postedTo'] = posted_to
    terms['api_key'] = api_key
    terms['ncode'] = ncode
    terms['pcode'] = ptype
    
    
    return terms


def init_search(terms):
    search = f"https://api.sam.gov/prod/opportunities/v2/search?api_key={terms.get('api_key')}"

    for key, value in terms.items():
        if(key == 'api_key'):
            continue
        if not terms.get(key):
            continue
        
        if isinstance(terms.get(key), list):
            for search_term in value:
                search += f"&{key}={search_term}"
        else:
            search += f"&{key}={value}"
    
    return search

if __name__=="__main__":
    
    terms = init_search_terms(ncode=541330, ptype=['r', 'o', 's', 'k'])
    search = init_search(terms)
    
    response = requests.get(search)
    results_json = response.json()
    
    if results_json.get('error'):
        print(results_json.get('error').get('message'))
        print("Exiting with error.")
        exit(1)
        
    # sets opp_list to a list of dictionaries, one for each opportunity
    opp_list = results_json['opportunitiesData']
        
    for opp_dict in opp_list:
        print(opp_dict.get('title'))
        print("___________\n")
        
    print(opp_list[0])

    
    # print(results.json())
    
    