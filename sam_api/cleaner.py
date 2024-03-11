import pandas as pd

def remove_cols(df):
    df = df.drop(columns=['fullParentPathCode', 'archiveType', "archiveDate",
                     "naicsCodes", "organizationType", "officeAddress", "active"])
    return df

def remove_inactive(df):
     df = df.loc[df['active'] == "Yes"]
     
     return df
 
def check_set_aside(df):
     df = df.loc[(df['typeOfSetAside'] == "SBA") | df['typeOfSetAside'].isnull()]
     return df

#return valid contracts
def validate(df):
    df = remove_inactive(df)
    df = check_set_aside(df)
    # MUST BE LAST
    df = remove_cols(df)
    
    return df

def readable(df):
     #TODO: implement
     return df