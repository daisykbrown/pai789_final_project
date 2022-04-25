#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 15:14:21 2022

@author: daisybrown and Peter Wilcoxen
"""

import geopandas as gpd
import geotools  ### TWEAK 1

# setting the output file
out_file = "flood_levels.gpkg"

# setting a projection variable
nc_epsg = 2264

# reading in the approproate shape files
# make sure to create a path that works with where your data is saved

bfe_file = "../GIS/County Flood Hazard Layers/FEMA_Flood_HAZ_ColumbusCounty/S_BFE.shp"

fldhzrd_file = "../GIS/County Flood Hazard Layers/FEMA_Flood_HAZ_ColumbusCounty/S_FLD_HAZ_AR.shp"

# setting the projection for bfe and fldhzrd

bfe = gpd.read_file(bfe_file)

bfe = bfe.to_crs(epsg=nc_epsg)

fldhzrd = gpd.read_file(fldhzrd_file)

fldhzrd = fldhzrd.to_crs(epsg=nc_epsg)

# pulling out the 100 year flood zone

in_100 = fldhzrd["FLD_ZONE"].str.startswith("A")

fld100 = fldhzrd[in_100]

#%%
# using the disolved method 

dissolved = fld100.dissolve('STATIC_BFE')
dissolved = dissolved.reset_index()

vor_target = dissolved.query('STATIC_BFE < 0')

# adding layers to geopackage

fld100.to_file(out_file, layer="floodzone", index=False)

bfe.to_file(out_file, layer="bfe", index=False)

dissolved.to_file(out_file, layer="dissolve", index=False)

#%%

new_bfe = geotools.to_points(bfe[['ELEV','geometry']],step=200)
new_bfe.to_file(out_file,layer='bfe_points',index=False)
print( 'BFE points created', len(new_bfe) )

vor = geotools.voronoi(new_bfe)
print( 'Voronoi polygons created', len(vor) )

#%%

#adjust the buffer size as needed in feet by changing values in buffer_size

buffer_size = 5000

dis_bfe = new_bfe.dissolve()
buf_bfe = dis_bfe.buffer(buffer_size)
clip_vor = vor.clip(buf_bfe,keep_geom_type=True)
dis_vor = clip_vor.dissolve('ELEV').reset_index()

dis_vor.to_file(out_file,layer='voronoi',index=False)
print( 'Voronoi elevations created', len(dis_vor) )

#%%

ele_poly = dis_vor.overlay(vor_target[['geometry']],how='intersection')
#ele_poly.to_file(out_file,layer='flood_elev',index=False)
print( 'Flood elevations created', len(ele_poly) )

#%%

# adding the BFEs from FEMA flood map onto the elevation polygons

known_bfe = dissolved.query('STATIC_BFE > 0')

known_bfe = known_bfe[['STATIC_BFE', 'geometry']]

finished = ele_poly.append(known_bfe)

finished.to_file(out_file,layer='flood_elev',index=False)