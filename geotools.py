"""
@author: Peter Wilcoxen
"""

import geopandas as gpd
import scipy.spatial
import shapely.geometry

from shapely.geometry import MultiPoint

#
#  lineseg_to_points
#

#%%
def lineseg_to_points(geo,step=100):
    
    pts = []
    
    last = None
    for i,t in enumerate(geo.coords):
        if i>0:
            dx = t[0]-last[0]
            dy = t[1]-last[1]
            dist = ( dx**2 + dy**2 )**0.5
            nseg = 1 + int(dist/step)
            if nseg>1:
                for n in range(1,nseg):
                    shr = n/nseg
                    int_pt = (last[0]+dx*shr,last[1]+dy*shr)
                    pts.append(int_pt)
        pts.append(t)
        last = t
        
    return MultiPoint(pts)

#
#  to_points
#

#%%
def to_points(geodata,step=100):
    
    cur_geo = geodata['geometry']
    new_geo = cur_geo.apply(lambda g: lineseg_to_points(g,step))

    new_geodata = geodata.copy()
    new_geodata['geometry'] = new_geo

    new_geodata = new_geodata.explode(ignore_index=True)

    return new_geodata


#
#  voronoi
#

#%%
def voronoi(geodata):

    coord = [ (v.x,v.y) for v in geodata['geometry'] ]

    vor = scipy.spatial.Voronoi(coord)

    poly_list = []
    
    for pt in range(len(coord)):

        p_reg = vor.point_region[pt]
        v_reg = vor.regions[p_reg]

        pts = []
        for vp in v_reg:
            if vp != -1:
                pts.append( vor.vertices[vp] )
        pts.append( pts[0] )

        ls = shapely.geometry.LineString(pts)
        po = shapely.geometry.Polygon(ls)

        poly_list.append( po )

    new_geo = gpd.GeoSeries(poly_list)
    new_geo = new_geo.set_crs(geodata.crs)
    
    res = geodata.copy()
    res['geometry'] = new_geo
    
    return res
