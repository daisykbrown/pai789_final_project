"../Input Files/Columbus_FP.gdb"
import geopandas as gpd
import os

#
#  Input files
#

building_file = "./Input Files/Columbus_FP.gdb"

fema_file = "./Input Files/FEMA_Flood_HAZ_ColumbusCounty.zip"

#
#  Output file
#

out_file = 'floodplain-buildings.gpkg'

if os.path.exists(out_file):
    os.remove(out_file)
    
#%% Building footprints


building = gpd.read_file(building_file,layer='Columbus_FP')

#%% FEMA layers

fema_fld = gpd.read_file(fema_file+'!S_FLD_HAZ_AR.shp')
fema_bfe = gpd.read_file(fema_file+'!S_BFE.shp')
fema_xs  = gpd.read_file(fema_file+'!S_XS.shp')

fema_fld = fema_fld.to_crs(building.crs)
fema_bfe = fema_bfe.to_crs(building.crs)
fema_xs  = fema_xs.to_crs(building.crs)

#%% FEMA A zone

fema_a = fema_fld[ fema_fld['FLD_ZONE'].str.startswith('A') ]
fema_a = fema_a[['FLD_ZONE','STATIC_BFE','geometry']]

has_bfe = fema_a['STATIC_BFE']>0
fema_a_static = fema_a[ has_bfe ]
fema_a_other = fema_a[ has_bfe==False ]

#%% Buildings in the A zones

in_flood = building.sjoin(fema_a,how='left',predicate='intersects')
in_flood = in_flood.drop(columns='index_right')

#%% Save layers

in_flood.to_file(out_file,layer='buildings',index=False)
fema_a_static.to_file(out_file,layer='floodplain-bfe',index=False)
fema_a_other.to_file(out_file,layer='floodplain-nobfe',index=False)
fema_bfe.to_file(out_file,layer='bfe',index=False)
fema_xs.to_file(out_file,layer='xs',index=False)
