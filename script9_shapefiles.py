#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 11 14:52:51 2022

@author: daisybrown
"""

# writing shapefiles for Tableau

import script3_geotools as geotools
import geopandas as gpd


# saving ftp_demo_tax layer as shapefile

Ftp_Demo_Tax_Depth_file = "flood_levels.gpkg"

ftp_demo_tax = gpd.read(Ftp_Demo_Tax_Depth_file, layer = "ftp_demo_tax")

joined_tax_shp = geotools.to_shapefile(ftp_demo_tax,"Ftp_Demo_Tax.zip")

#%%

# saving flood depth layer as shapefile

flood_depth = gpd.read(Ftp_Demo_Tax_Depth_file, layer = "flood_depth")
flood_depth_shp = geotools.to_shapefile(flood_depth,"Flood_Depth.zip")

#%%

# saving floodplain map to shapefiles
flood_file = "flood_sections_static.gpkg"

flood_depth_sections = gpd.read(flood_file, layer = "sections")

sections_shp = geotools.to_shapefile(flood_depth_sections,"Sections.zip")

flood_depth_static = gpd.read(flood_file, layer = "static")

static_shp = geotools.to_shapefile(flood_depth_static,"Static.zip")
