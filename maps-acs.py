"""
Plot some maps of Census variables.

Sep 2021 PJW
"""

import geopandas as gpd
import matplotlib.pyplot as plt

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

elev = gpd.read_file("flood_levels.gpkg", layer = "flood_elev")

for geo in ['tracts','bgs']:

    #  Read the relevant layer
    
    demo = gpd.read_file("flood_levels.gpkg", layer = "county")

    #  Try to draw everyting
        
    draw_map(demo,geo,'pop_nonwhite_pct','Percent of Population Nonwhite')
    draw_map(demo,geo,'occ_occupied_pct','Percent of homes Occupied')
    draw_map(demo,geo,'own_occupied_pct','Percent of homes Owner-Occupied')
    draw_map(demo,geo,"age_below5_pct",'Percent of People Below Age 5')
    draw_map(demo,geo,"age_above65_pct",'Percent of People Above Age 65')
    draw_map(demo,geo,'median_income','Median Income')
    draw_map(demo,geo,'unemployed_pct','Percent of People Unemployed')
    draw_map(demo,geo, "pct_povinc_below2",'Percent of Families 2X Below Poverty Level')
    draw_map(demo,geo, 'second_lang_poor_pct','Percent of Non-English Speakers')

              
              

