# pai789_final_project_dev

# Investigating Flood Risk and Equity in North Carolina

## Background

As temperatures increase, communities across the globe are expected to experience more extreme weather events. In North Carolina, the state currently experiences both coastal and inland flooding, and is expected to have more flood events due to climate change. Smaller, lower-resourced populations are specifically going to experience the brunt of climate impacts because as these communities experience more natural disasters, residents and employers leave and their tax bases dwindle, thus making it harder to fund basic services. This repository investigates Columbus County specifically, but future work can utilize the resources included as a foundation to build upon. This repository was created with the goal of helping policy makers and communities better understand their flood risk. Specifically, this repository uses data from FEMA, the state of North Carolina, and the U.S. Census Bureau to calculate: 

1) The expected depth of flooding (in feet) for parcels that stand in FEMA’s 1% annual flood chance zone

2) Block group-level demographic characteristics that were chosen based on the Environmental Protection Agency’s (EPA) Environmental Justice Indicators. These demographics are at the block-group level and include: 
  * The percent of the population that is non-white hispanic
  * The percent of households where the household income is less than or equal to twice the federal "poverty level”
  * The unemployment rate
  * The percent of households who do not speak English or do not speak English “very well”
  * The percent of people age 25 or older in a block group whose education is short of a high school diploma
  * The percent of people who are under age 5
  * The percent of people who are over age 5

The block-group characteristics not guided by the EPA’s Environmental Justice Indicators but also included in the analysis are:
  * The percent of buildings occupied
  * The percent of buildings owner-occupied
  * Median Income


## Folder Structure:
All scripts will be found within folders that include the script and any input files. Each script folder will have a number in the front, which indicates the order in which the scripts should be run.

## Scripts

The scripts of this repository do the following:

### Script1: nc_acs.py

#### A. Summary
This script uses request and pandas modules of Python. The script does the following:
Pulls appropriate demographic data from the ACS from 2018 for your desired county and state identified by the appropriate FIPS codes. These demographics will be used in script2 to calculate the appropriate demographics inspired by the EPA’s Environmental Justice Indicators. 
Creates two new csv files for block groups (“nc-census-acs-bgs.csv”) and tracts (“nc-census-acs-tracts.csv”). These csv files will be used in script 2

#### B. Input Data
There input data for this script:
"NC_ACS_2018_Shells_FLD.csv" which is a csv of the desired demographic data taken from the ACS 2018 Table Shells and shortened to the appropriate demographics. The 2018 Table Shells for the ACS can be found here: https://www.census.gov/programs-surveys/acs/technical-documentation/table-shells.2018.html 

### Script2: analyze-acs-nc.py

#### A. Summary
This script uses pandas, geopandas,and numpy modules of Python. The script does the following:
Reads the bg and tract csvs created in script1 and calculates the demographics that will be utilized in the analyisis. The script breaks these up by block group and by tract. The tract group variables will be percentages and can therefore be assigned to the block groups.
Merges the block group and tract level data into one csv titled "nc_bg_tract_merged.csv"

#### B. Input Data
There input data for this script:
nc-census-acs-bgs.csv
nc-census-acs-tracts.csv
 
 
### Script3: geotools.py 

#### A. Summary
This script is written by Profesor Peter Wilcoxen and uses geopands and scipy.spatial and shapely.geometry modules of Python and also imports MultiPoint from shapely.geometry. The script does the following:
Defines a module called “geotools” that will be utilized in script 5.


### Script4: flood_plain_buildings.py

#### A. Summary
This script was written by Peter Wilcoxen and uses geopands and os module of Python. The script does the following:
Creates a new geopackage file titled “floodplain-buildings.gpkg” that will hold all of the QGIS layers that are used to build the floodplain.
The layers in the geopackage are:
  * buildings: a layer that includes all buildings from the Columbus_FP.gd file that intersect with the floodplain
  * floodplain-bfe: a layer of the areas that do have BFE within the floodplain
  * floodplain-nobfe: a layer of the areas that do not have BFEs within the floodplain
  * bfe: a layer with all of the BFEs with elevations in the FEMA zip file that correspond to 'S_BFE.shp'
  * xs: a layer with all of the XS lines with elevations in the FEMA zip file that correspond to 'S_XS.shp'
  
The input files used in this script are: 
  * 'Columbus_FP.gdb' which provides information for buildings in Columbus County, such as the LIDAR_LAG value used to calculate the expected flood depth.
  * 'FEMA_Flood_HAZ_ColumbusCounty.zip' which provides the FEMA Flood Zone shape files used to construct the flood zone in the county
   

### Script5: flood_plain_buildings.py

#### A. Summary

This script was written by Peter Wilcoxen and uses geopands and pandas modules of Python as well as the geotools module created in Script3. The script uses voronois and dissolves to produces a new geopackage titled 'flood-elevation-points.gpkg'.

The input file used is:
 * 'floodplain-buildings.gpkg' which is the geopackage created in Script4

### Script6: join_parcel_demo.py

#### A. Summary
This script uses geopands module of  Python and geotools created in the script 3. The script does the following:
Creates a new geopackage file titled “flood_levels.gpkg” that will hold all of the QGIS layers that will be used in the analysis. The layers created in the geopackage are:


### Script7: flood_depth.py
#### A. Summary
This script isuses geopands module of  Python and geotools created in the script 3. The script does the following:
Creates a new geopackage file titled “flood_levels.gpkg” that will hold all of the QGIS layers that will be used in the analysis. The layers created in the geopackage are:


### Script7: maps-acs.py 

#### A. Summary
This script isuses geopands module of  Python and geotools created in the script 3. The script does the following:
Creates a new geopackage file titled “flood_levels.gpkg” that will hold all of the QGIS layers that will be used in the analysis. The layers created in the geopackage are:



## Data Files 
Data files within the repository are sourced from various resources. The appropriate input files will be held within the repository, but you will find instructions below on how to source the data used in this project:

### North Carolina Spacial Data Download:

  * The data from this site include Building Footprint data and DEM data
  * You will have to create an account here to access the data: https://sdd.nc.gov
  * Once logged in, select “County” 
  
  ![Selecting County From SDD Site](County.png)
  
  * Then select “Click Here to Download Countywide Data”
  ![Download County Data from SDD Site](LargeDataRequest.png)
  
  * From there, select “Columbus” and the selection will appear in the “Requested Areas” box
  ![Selecting Columbus County from SDD Site](Columbus_SDD.png)
  
  
 
