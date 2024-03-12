def convert_location(d):
    if not d:
        return ''
    
    
    city = d.get('city')
    if city: city = city.get('name')
        
    state = d.get('state')
    if state: state = state.get('code')
    
    country = d.get('country')
    if country: country = country.get('code')
    
    loc = ""
    if city: loc += f"{city}, "
    if state: loc += f"{state}, "
    if country: loc += f"{country}, "
    if loc: loc = loc[:len(loc) - 2]
    
    return loc

def readable(df):
     # drop all columns that can't be serialized for sheets
     df = df.drop(columns=['award', 'pointOfContact', 'links', 'resourceLinks'])
     # drop columns that can't be read
     df = df.drop(columns=['description'])
     # drop columns that are redundant
     df = df.drop(columns=['typeOfSetAsideDescription'])
     # drop unecessary columns:
     df = df.drop(columns=['additionalInfoLink'])
     
     df['placeOfPerformance'] = df['placeOfPerformance'].apply(convert_location)
     
     return df