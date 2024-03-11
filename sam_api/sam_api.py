import requests
import os
import json
import datetime
import pandas as pd
import cleaner

def init_search_terms(limit=100, posted_from=None,
                      posted_to=None, ptype=None, ncode=None):
    api_key = os.getenv('SAM_API_KEY')
    print(api_key)
    if not api_key:
        print("Valid API Key not found")
        exit(-1)
    
    if not posted_to:
        posted_to = datetime.date.today().strftime("%m/%d/%Y") 
        
    if not posted_from:
        posted_from = posted_to

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

def main():
    DEBUG = False
    
    terms = init_search_terms(ncode=541330, ptype=['r', 'o', 's', 'k'])
    search = init_search(terms)
    if DEBUG: print(search)
    
    response = requests.get(search)
    results_json = response.json()
    
    if results_json.get('error'):
        print(results_json.get('error').get('message'))
        print("Exiting with error.")
        exit(1)
    
    if DEBUG: print(results_json)
    # sets opp_list to a list of dictionaries, one for each opportunity
    opp_list = results_json['opportunitiesData']
     
    if DEBUG:   
        for opp_dict in opp_list:
            print(opp_dict.get('title'))
            print("___________\n")
        
    df = pd.DataFrame.from_records(opp_list)
    if DEBUG:
        for col in df.columns: print(col)
    df = cleaner.validate(df)
    date = str(datetime.date.today())
    df.to_csv(f"./results/{date}.csv")
    if DEBUG: print(df)
    
    return df
    
if __name__=="__main__":
    main()

    
    