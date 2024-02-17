import requests
import os
import json

def init_search():
    api_key = os.getenv('SAM_API_KEY')
    if not api_key:
        print("Valid API Key not found")
        exit(-1)
    
    
    terms = {}
    terms['api_key'] = api_key
        
    search = f"https://api.sam.gov/prod/opportunities/v2/search?limit=5&api_key={terms.get('api_key')}&postedFrom=01/01/2024&postedTo=05/10/2024&ptype=a&deptname=general"
    return search

if __name__=="__main__":
    
    search = init_search()
    
    response = requests.get(search)
    results_json = response.json()
    
    if results_json.get('error'):
        print(results_json.get('error').get('message'))
        print("Exiting with error.")
        exit(1)
        
    # sets opp_list to a list of dictionaries, one for each opp
    opp_list = results_json['opportunitiesData']
        
    for opp_dict in opp_list:
        print(opp_dict.get('title'))
        print("___________\n")
        
    print(opp_list[0])

    
    # print(results.json())
    
    