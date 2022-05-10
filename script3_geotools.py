"../Input Files/Columbus_FP.gdb"
import geopandas as gpd
import matplotlib.pyplot as plt
import shapely.validation
from shapely.geometry import Point, MultiPoint
import shutil
import time

#
#  lineseg_to_points
#

def lineseg_to_points(geo,step=None):
    
    if step is None:
        return MultiPoint(geo.coords)
    
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

def to_points(geodata,step=None):
    
    cur_geo = geodata['geometry']
    new_geo = cur_geo.apply(lambda g: lineseg_to_points(g,step))

    new_geodata = geodata.copy()
    new_geodata['geometry'] = new_geo

    new_geodata = new_geodata.explode(ignore_index=True)

    return new_geodata


#
#  voronoi
#

def voronoi(geodata):

    #  Get the coordinates for all the features
    
    coords = [ (v.x,v.y) for v in geodata['geometry'] ]
    
    #  Do the main voronoi calculations

    mp = MultiPoint( coords )
    vor = shapely.ops.voronoi_diagram(mp,edges=False)    
     
    poly_list = [p for p in vor.geoms]

    new_geo = gpd.GeoDataFrame(geometry=poly_list)
    new_geo = new_geo.set_crs(geodata.crs)
    
    res = new_geo.sjoin(geodata,how='left',predicate='contains')
    res = res.drop(columns='index_right')
    
    return res
    
#
#  make_valid
#
#     Changes data in place
#

def make_valid(geodata):
    is_ok = geodata.is_valid
    if is_ok.all():
        return geodata
    n = (is_ok == False).sum()
    print(f'Correcting {n} invalid geometries')
    geodata.geometry = [ shapely.validation.make_valid(g) for g in geodata.geometry ]

#
#  save to a zipped shapefile  
#

def to_shapefile(geo,zipname):
    stem = zipname.replace('.zip','')
    geo.to_file( stem )
    shutil.make_archive(stem,'zip',stem)
    time.sleep(1)
    shutil.rmtree(stem)


#
#  tests if run directly
#

if __name__ == "__main__":

    test = [
        {'c':'tan'   ,'geometry':Point(1,1)},
        {'c':'yellow','geometry':Point(1,2)},
        {'c':'olive' ,'geometry':Point(2,1)},
        {'c':'orange','geometry':Point(2,2)},
        {'c':'aqua'  ,'geometry':Point(1.5,1.5)}
        ]

    ser = gpd.GeoDataFrame(test)
    ser = ser.set_crs(epsg=4326)

    vor = voronoi(ser)
    print(vor)
    
    fig,ax1 = plt.subplots()
    vor.plot(color=vor['c'],ax=ax1)
    ser.plot(color='black',ax=ax1)
    fig.tight_layout()
