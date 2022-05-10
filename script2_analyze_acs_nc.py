# -*- coding: utf-8 -*-

"""

@author: Peter Wilcoxen and daisybrown 
"""

import pandas as pd
import numpy as np 

for geo in ['tracts','bgs']:

    #
    #  Initialize things for this geometry
    #
    
    ifile = f'nc-census-acs-{geo}.csv'
    ofile = f'analyze-acs-{geo}-nc.csv'

    raw = pd.read_csv(ifile,dtype={'geoid':str})
    raw = raw.set_index('geoid')
    
    mod = raw.replace({-666666666:np.nan})
    dif = (raw != mod).sum().sum()
    print(f'Processing {geo}: replaced {dif} missing values with NaNs')
    raw = mod 
    
    res = pd.DataFrame()
    
    #
    #  Calculations supported for block groups and tracts
    #
    
    res['pop_all'] = raw['B02001_001E']
    res['pop_white'] = raw['B02001_002E']
    res['pop_nonwhite_pct'] = 100*(1-res['pop_white']/res['pop_all'])
    
    #  Calculations for occupied and vacant buildings
    res['occ_all'] = raw['B25002_001E']
    res['occ_occupied'] = raw['B25002_002E']
    res['occ_occupied_pct'] = 100*(res['occ_occupied']/res['occ_all'])
    
    #   Calculations for owner occupied buildings
    res["tenure"] = raw['B25003_001E']
    res['own_occupied_pct'] = 100* raw["B25003_002E"] / res['tenure'] 
    
   
    #  That's it if we're doing block groups. Subsequent calculations
    #  are only supported for tracts. Save and continue.
    #

  
    #  Age below 5
    res["age_total"] = raw["B01001_001E"]
    res["age_below5"] = raw["B01001_003E"] + raw["B01001_027E"]
    res["age_below5_pct"] =  100* res["age_below5"] / res["age_total"]
    
    #  Age above 65
    res["age_above65"] = raw["B01001_020E"] + raw["B01001_021E"] + raw["B01001_022E"] 
    + raw["B01001_023E"] +  raw["B01001_024E"] + raw["B01001_025E"] + raw["B01001_044E"]
    + raw["B01001_045E"] + raw["B01001_046E"] + raw["B01001_047E"] + raw["B01001_048E"] 
    + raw["B01001_049E"]
    res["age_above65_pct"] = 100* res["age_above65"] /  res["age_total"]
  
    
    #   Median Income
    res['median_income'] = raw['B19013_001E']
    
    
    #   Education
    res['ed_all'] = raw['B15003_001E']
    
    res['ed_less_highschool'] = raw['B15003_002E']+ raw['B15003_002E'] + raw['B15003_003E']
    + raw['B15003_004E'] + raw['B15003_005E'] + raw['B15003_006E'] + raw['B15003_007E'] 
    + raw['B15003_008E'] + raw['B15003_009E'] + raw['B15003_010E'] + raw['B15003_011E']
    + raw['B15003_012E'] + raw['B15003_013E'] + raw['B15003_014E'] + raw['B15003_015E'] 
    + raw['B15003_016E']
    
    res['ed_highschool_GED'] = raw['B15003_017E'] + raw['B15003_018E']
    res['ed_some_college_plus'] =  res['ed_all']- res['ed_less_highschool']- res['ed_highschool_GED']
    res['ed_highschool_below_pct'] = 100*((res['ed_highschool_GED']+res['ed_less_highschool'])/ res['ed_all'])
    
    
    # EMPLOYMENT STATUS FOR THE POPULATION 16 YEARS AND OVER
    res['employ_total'] = raw["B23025_001E"]
    res["unemployed"] = raw["B23025_005E"]
    res['unemployed_pct'] = 100* res["unemployed"] / res['employ_total']
    
    res = res[['pop_nonwhite_pct',
               'occ_occupied_pct', 
               'own_occupied_pct',
               "age_below5_pct",
               "age_above65_pct",
               'median_income',
               'ed_highschool_below_pct',
               'unemployed_pct']]
    
    
    if geo == 'bgs':
         res.to_csv(ofile)
         continue
        
    #
    #  Tract calculations follow
    
    
    
    #   RATIO OF INCOME TO POVERTY LEVEL OF FAMILIES IN THE PAST 12 MONTHS in familes
    #   No blockgroups
    res["povinc_ratio_total"] = raw["B17026_001E"]
    res["povinc_ratio_above2"] = raw["B17026_010E"] + raw["B17026_011E"] + raw["B17026_012E"]
    + raw["B17026_013E"]
    res["povinc_ratio_below2"] = res["povinc_ratio_total"] - res["povinc_ratio_above2"]
    res["pct_povinc_below2"] = 100* res["povinc_ratio_below2"] / res["povinc_ratio_total"]
   
   
    #All English Proficiency
    
    res['all_eng_all'] = raw['B06007_001E']
    res['all_eng_primary'] = raw['B06007_002E']
    res['all_eng_second_good'] = raw['B06007_004E'] + raw['B06007_007E']
    res['all_eng_second_poor'] = raw['B06007_005E'] + raw['B06007_008E']
    res['pct_limited_eng'] = 100*res['all_eng_second_poor']/ res['all_eng_all']
    
    
    #
    #  Done, write the output
    #
    
    res = res[["pct_povinc_below2",
               'ed_highschool_below_pct',
               'unemployed_pct',
               'pct_limited_eng']]
    
    res.to_csv(ofile)
    

#%%

bg = pd.read_csv('analyze-acs-bgs-nc.csv')

tract = pd.read_csv('analyze-acs-tracts-nc.csv')

bg['geoid'] = bg['geoid'].astype(str)

bg["tractid"] = bg["geoid"].str[:11]

tract["tractid"] = tract["geoid"].astype(str)

tract = tract.drop(columns=['geoid', 'ed_highschool_below_pct', 'unemployed_pct'])

bg = bg.merge(tract, on="tractid", how='left', validate='m:1')

bg.to_csv("nc_bg_tract_merged.csv")
