# -*- coding: utf-8 -*-

"""
@author: daisybrown
"""
import pandas as pd
import geopandas as gpd


# setting the output file
out_file = "flood_levels.gpkg"

# setting a projection variable
nc_epsg = 2264


# reading in the approproate shape files for FFE
fp_file = "../GIS/County Building Data/Columbus_FP_Info.gpkg"

# setting the projection

fp = gpd.read_file(fp_file)

fp = fp.to_crs(epsg=nc_epsg)

# trimming the geospatial data for relevent columns

trim_fp = fp.copy()

trim_fp = trim_fp[['FFE', 'geometry']]

#trim_fp['STATIC_BFE'] = trim_fp['STATIC_BFE'].astype(float)

#%%

# reading in the FEMA flood elevations NC One Data
flood = gpd.read_file("flood_levels.gpkg", layer = "flood_elev")

flood.info()

# setting the projection 
    
flood = flood.to_crs(epsg=nc_epsg)

# trimming the geospatial data for relevent columns

#%%

joined = trim_fp.sjoin(flood, how='left', predicate='within')

joined = joined.drop(columns='index_right')

joined['flood_depth'] = joined['ELEV'] - joined['FFE']

joined["depth1"] = joined['ELEV'] - joined['FFE']
depth1 = joined["depth1"]

joined["depth2"] = joined['STATIC_BFE'] - joined['FFE']

depth2 = joined["depth2"]

joined['flood_depth'] = depth1.where( depth1.notna(), depth2 )

joined = joined.drop(columns=['depth1', 'depth2'])

joined.to_file(out_file, layer = "flood_depth", index=False)
