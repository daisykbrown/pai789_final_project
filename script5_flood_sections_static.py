import geopandas as gpd
import pandas as pd 
import geotools3 as geotools

in_file = 'floodplain-buildings.gpkg'
out_file = 'flood_sections_static.gpkg'

#%% Inputs
#
#  Read the input layers
#

fema_a_nobfe = gpd.read_file(in_file,layer='floodplain-nobfe',index=False)

fema_bfe = gpd.read_file(in_file,layer='bfe',index=False)
fema_bfe['source'] = 'BFE'

fema_xs = gpd.read_file(in_file,layer='xs',index=False)
fema_xs['source'] = 'XS'

#
#  Build a stripped-down combined layer
#

sel_bfe = fema_bfe[['ELEV','source','geometry']]

sel_xs = fema_xs[['WSEL_REG','source','geometry']].copy()
sel_xs = sel_xs.rename(columns={'WSEL_REG':'ELEV'})

stack = pd.concat( [sel_bfe,sel_xs], ignore_index=True )

#
#  Write it out
#

stack.to_file('bfe-xs.gpkg',layer='combined',index=False)

#%% Voronois
#
#  Build the point version, the voronois, the dissolved voronois,
#  and write each layer out
#

def write(geo,layer):
    num = len(geo)
    print(f'Writing {num} features to layer',layer,flush=True)
    geo.to_file(out_file,layer=layer,index=False)
    
print('\nBuilding points',flush=True)
pts = geotools.to_points(stack)
write(pts,'points')

print('\nBuilding voronois',flush=True)
vor = geotools.voronoi(pts)
write(vor,'voronoi')

print('\nDissolving voronois',flush=True)
dis = vor.dissolve('ELEV')
dis = dis.reset_index()
write(dis,'dissolved')

#%% Slices
#
#  Now slice the floodplain and write that out, too
#

print('\nDissolving the non-BFE floodplain',flush=True)
fema_a_dis = fema_a_nobfe.dissolve()
write(fema_a_dis,'nobfe_dis')

print('\nBuilding overlay',flush=True)
sec = fema_a_dis.overlay(dis,how='intersection',keep_geom_type=True)
write(sec,'sections')

#%% Static
#
#  Finally, copy over the static BFE part of the floodplain
#

fema_a_static = gpd.read_file(in_file,layer='floodplain-bfe',index=False)
write(fema_a_static,'static')