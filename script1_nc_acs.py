#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 18:11:27 2022

@author: Peter Wilcoxen and daisybrown 
"""

import requests
import pandas as pd

acs_yr = 2018

ifile = "./Input Files/NC_ACS_2018_Shells_FLD.csv"

#%%

for geo in ['tracts','bgs']:

    ostem = f"nc-census-acs-{geo}"
    
    #
    #  Read the auxiliary file containing the list of variables and 
    #  the groups they should be aggregated into.
    #
    
    var_info = pd.read_csv(ifile)
    
    var_info.dropna(axis=0,subset=['UniqueID'],inplace=True)
    var_info['table'] = var_info['Table ID']
    var_info['variable'] = var_info['UniqueID']+'E'
    
    #  
    #  No block groups for tables with a couple of entries in the 
    #  geographic restrictions column. Probably applies for ANY 
    #  non-blank entry in that column but the documentation is a 
    #  little unclear.
    #
    
    if geo == 'bgs':
        var_info = var_info[ var_info['Geo Res'] != 'No Blockgroups' ]
        var_info = var_info[ var_info['Geo Res'] != 'Place of Work Only' ]
    
    #%%
    #
    #  Set up the components of the API call. This omits my Census
    #  API key since the code will be posted on the web.
    #
    
    api = f"https://api.census.gov/data/{acs_yr}/acs/acs5"
    
    for_clause = 'tract:*'
    if geo == 'bgs':
        for_clause = 'block group:*'
        
    in_clause = 'county:047 state:37'
    key_value = 'fb5a632a6a691a18afb5acba2a4a5696c2ab677c'
    
    #%%
    
    grps = var_info.groupby('table')
    files = []
    
    for table,table_info in grps:
        
    #
    #  Get the names of the variables and build a string of 
    #  variable names that can be passed to the Census API.
    #
    
        var_name = table_info['variable'].to_list()
        var_list = ['NAME']+var_name
        var_string = ','.join(var_list)
    
        #
        
        payload = {'get':var_string,'for':for_clause,'in':in_clause,'key':key_value}
    
        #
        #  Make the API call and check whether an error code was 
        #  returned.
        #
    
        response = requests.get(api,payload)
    
        if response.status_code == 200 :
            print('Request successful')
        else:
            print('Returned status:',response.status_code)
            print('Returned text:',response.text)
            assert False 
    
        #
        #  The results are in JSON. Parse the JSON into a Python object. 
        # It will be a list of rows, each of which is itself a list.
        #
    
        row_list = response.json()
    
        #
        #  The first row is the column names and the remaining rows are the data.
        #
    
        colnames = row_list[0]
        datarows = row_list[1:]
    
        #
        #  Build a Pandas dataframe and a geoid field
        #
    
        data = pd.DataFrame(columns=colnames,data=datarows)
    
        st = data['state']
        co = data['county']
        tr = data['tract']
        
        data['geoid'] = st+co+tr
        if geo == 'bgs':        
            data['geoid'] += data['block group']
        
        data['table'] = table.lower()
    
        data.set_index('geoid',inplace=True)
        
        #  
        #  Warn about empty variables
        #
        
        ndrop = 0
        for v in var_name:
            if data[v].isna().all():
                print(f'Warining: {v} has no data and was dropped')
                data = data.drop(columns=v)
                ndrop += 1
    
        #
        #  Write out the results.
        #
    
        if len(var_name) == ndrop:
            print(f'Warning: no remaining variables for {table} so no file written.')
        else:            
            fname = f'raw/{table.lower()}-{geo}.csv'
            data.to_csv(fname)
            files.append( fname )
    
    #%%
    
    ofile = ostem+'.csv'
    
    merged = pd.DataFrame()
    
    for f in files:
        print('Merging file',f)
        this = pd.read_csv(f,dtype=str)
        this = this.drop(columns=['NAME','state','county','tract','table'])
        if geo == "bgs":
            this = this.drop(columns = "block group")
        if len(merged) == 0:
            merged = this
        else:
            merged = merged.merge(this,how='outer',on='geoid',validate='1:1',indicator=True)    
            check = merged['_merge'].value_counts()
            if check['left_only']>0 or check['right_only']>0:
                print('Warning: unexpected merge result')
                print(check)
            merged = merged.drop(columns='_merge')
    
    merged.to_csv(ofile,index=False)


