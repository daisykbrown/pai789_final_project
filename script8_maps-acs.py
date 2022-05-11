"""
Plot some maps of Census variables.

Sep 2021 PJW and Daisy Brown
"""
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt


# creating a county GIS layer
# setting the output file
out_file = "flood_levels.gpkg"

# setting a projection variable
nc_epsg = 2264

county_file = "./Input Files/cb_2019_us_county_500k.zip"

county = gpd.read_file(county_file)

county = county.to_crs(epsg=nc_epsg)

#nc = county.query("STATEFP=='37' & COUNTYFP=='047'").copy()

county = county[['STATEFP', 'COUNTYFP', 'GEOID', 'NAME', 'geometry']]

bg_file = "./Input Files/cb_2019_37_bg_500k.zip"

bg = gpd.read_file(bg_file)

bg = bg.to_crs(epsg=nc_epsg)

bg = bg[['STATEFP', 'COUNTYFP', 'GEOID', 'geometry']]

within = bg.sjoin(county, how='left', predicate='within')

demo = pd.read_csv("nc_bg_tract_merged.csv")

demo['geoid'] = demo['geoid'].astype(str)

demo = demo.set_index('geoid')

# joining demo data on trimmed fp data to create a new layer in the geopackage
# with the combined data

within_demo = within.merge(demo, 
                       left_on="GEOID_left", 
                       right_on="geoid", 
                       validate="m:1", 
                       indicator=True)

within_demo = within_demo[['STATEFP_left', 'COUNTYFP_left', 'GEOID_left', 'NAME', 
                           'pop_nonwhite_pct',
                           'occ_occupied_pct', 
                           'own_occupied_pct',
                           "age_below5_pct",
                           "age_above65_pct",
                           'median_income',
                           'ed_highschool_below_pct',
                           'unemployed_pct',
                           "pct_povinc_below2",
                           'pct_limited_eng',
                           'geometry']]

# print(within_demo.value_counts('_merge'))

# within_demo = within_demo.drop(columns='_merge')

within_demo.to_file(out_file,layer='county_demo',index=False)

#%%
#
#  Draw a map for a given variable
#

def draw_map(data,geo,var,title):
    
    #  Skip if variable isn't present
    
    if var not in data:
        print(f'Skipping missing variable for {geo}: {var}')
        return 
    
    #  Set up the figure
    
    fig, ax = plt.subplots(dpi=300)
    fig.suptitle(title)
    
    #  Plot the Census units
    
    data.plot(
        column=var,
        legend=True,
        cmap="RdYlBu_r",
        ax=ax
        )

    #  Draw the interstates on top
    
    elev.plot(
        color='black',
        linewidth=0.5,
        ax=ax)
    
    #  Tweak the axis and legend
    
    ax.axis('off')
    fig.axes[1].set_title(var)
    
    #  Save the result
    
    fig.tight_layout()
    
    figname = f'fig-{var}-{geo}.png'
    fig.savefig(figname)
    print('Drew',figname,flush=True)

#
#  Plot everything
#

elev = gpd.read_file("flood_sections_static.gpkg", layer = "sections")

for geo in ['tracts','bgs']:

    #  Read the relevant layer
    
    within_demo = gpd.read_file("flood_levels.gpkg", layer = "county_demo")

    #  Try to draw everyting
        
    draw_map(within_demo,geo,'pop_nonwhite_pct','Percent of Population Nonwhite')
    draw_map(within_demo,geo,'occ_occupied_pct','Percent of homes Occupied')
    draw_map(within_demo,geo,'own_occupied_pct','Percent of homes Owner-Occupied')
    draw_map(within_demo,geo,"age_below5_pct",'Percent of People Below Age 5')
    draw_map(within_demo,geo,"age_above65_pct",'Percent of People Above Age 65')
    draw_map(within_demo,geo,'median_income','Median Income')
    draw_map(within_demo,geo,'unemployed_pct','Percent of People Unemployed')
    draw_map(within_demo,geo, "pct_povinc_below2",'Percent of Families 2X Below Poverty Level')
    draw_map(within_demo,geo, 'second_lang_poor_pct','Percent of Non-English Speakers')

              
              

