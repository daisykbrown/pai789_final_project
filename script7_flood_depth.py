# -*- coding: utf-8 -*-

"""
@author: daisybrown
"""
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns


# setting the output file
out_file = "flood_levels.gpkg"

# setting a projection variable
nc_epsg = 2264


# reading in the approproate shape files for FFE
ftp_file = "../Input Files/Columbus_FP.gdb"

# setting the projection

ftp = gpd.read_file(ftp_file)

ftp = ftp.to_crs(epsg=nc_epsg)

# trimming the geospatial data for relevent columns

trim_ftp = ftp.copy()

trim_ftp = trim_ftp[['FFE', 'LIDAR_LAG', 'LIDAR_HAG','geometry']]

#%%

# reading in the FEMA flood elevations NC One Data
flood_file = "flood_sections_static.gpkg"
sections = gpd.read_file(flood_file, layer = "sections")
static = gpd.read_file(flood_file, layer = "static")


# setting the projection 
    
sections = sections.to_crs(epsg=nc_epsg)
static = static.to_crs(epsg=nc_epsg)

# trimming the geospatial data for relevent columns

#%%

joined = trim_ftp.sjoin(sections, how='left', predicate='within')

joined = joined.drop(columns='index_right')

joined["depth1"] = round(joined['ELEV'] - joined['LIDAR_LAG'],2)

depth1 = joined["depth1"]

#calibrate_static = 3.08

#joined["depth2"] = round(joined['STATIC_BFE'] - (joined['FFE'] - calibrate_static),2)

joined = joined.sjoin(static, how='left', predicate='within')

joined = joined.drop(columns='index_right')

FLD_ZONE_left = joined['FLD_ZONE_left']
FLD_ZONE_right = joined['FLD_ZONE_right']

joined["FLD_ZONE"] = FLD_ZONE_left.where (FLD_ZONE_left.notna(), FLD_ZONE_right)

joined = joined.drop(columns=['FLD_ZONE_left', 'FLD_ZONE_right'])

joined["depth2"] = round(joined['STATIC_BFE_right'] - joined['LIDAR_LAG'],2)

depth2 = joined["depth2"]

joined['flood_depth'] = depth1.where( depth1.notna(), depth2 )




joined = joined.drop(columns=['depth1', 'depth2', 'STATIC_BFE_left'])

joined.to_file(out_file, layer = "flood_depth", index=False)

#%%

# setting up classes to distinguish between positive and negative flood depths
# these classes can be used in the Tableau tool to easily distinguish between values

class1 = joined.query("flood_depth < 0")
class1 = class1[['LIDAR_LAG', 'flood_depth', 'geometry']]
class1 = class1.rename(columns={'flood_depth':'Class 1'})


class2 = joined.query("flood_depth >= 0")
class2 = class2[['LIDAR_LAG', 'flood_depth', 'geometry']]
class2 = class2.rename(columns={'flood_depth':'Class 2'})

class1.to_file(out_file, layer = 'class1', index=False)

class2.to_file(out_file, layer = 'class2', index=False)


# class3 = joined.query("flood_depth == 'nan'")
# class3 = class3[['LIDAR_HAG', 'flood_depth', 'geometry']]




#%%

# drawing a histogram of negative of negative values 

neg_depth = joined.query('flood_depth < 0')
print(neg_depth.value_counts('flood_depth'))
# create a new single-panel figure

neg_depth = neg_depth.reset_index()

fig, ax1 = plt.subplots(dpi=300)

# drawing a histogram of median earnings
# stat keyword indicates that the Y axis of the histogram should 
# be the probability density

sns.histplot(data=neg_depth, x="flood_depth", ax=ax1)

# The shade option causes the area below the curve to be shaded

ax1.set_xlabel("Negative Flood Depth")

fig.tight_layout()

fig.savefig("negdepth_hist.png")

#%%

# drawing a histogram of  of all depth values 

joined = joined.reset_index()

# create a new single-panel figure

fig, ax2 = plt.subplots(dpi=300)

# drawing a histogram of median earnings
# stat keyword indicates that the Y axis of the histogram should 
# be the probability density

sns.histplot(data=joined, x="flood_depth", ax=ax2)

# The shade option causes the area below the curve to be shaded

ax2.set_xlabel("All Flood Depths")

fig.tight_layout()

fig.savefig("alldepth_hist.png")