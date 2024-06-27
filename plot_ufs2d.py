#!/usr/bin/env python 
##########################################################################################
import numpy as np
import xarray as xr
import os
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.feature import ShapelyFeature, NaturalEarthFeature
from netCDF4 import Dataset

# Colormaps to use?
cmap_div = plt.cm.bwr
cmap_seq = plt.cm.YlGnBu

# Number of levels for plots?
nlev = 10
nlevd = 25

# Dictionary of variable(s) to plot
var_dict = [\
            {"name":"tmpsfc",       "range":[250, 340], "drange":[-.2,.2]}]#, \
            #{"name":"tmp2m",        "range":[250, 340], "drange":[-.2,.2]}, \
            #{"name":"ulwrf_ave",    "range":[200, 600], "drange":[-.5,.5]}, \
            #{"name":"ulwrf_avetoa", "range":[  1, 400], "drange":[-.1,.1]}, \
            #{"name":"uswrf_ave",    "range":[  1, 500], "drange":[-1,1]},   \
            #{"name":"uswrf_avetoa", "range":[  1,1000], "drange":[-1,1]},   \
            #{"name":"dlwrf_ave",    "range":[ 10, 500], "drange":[-.1,.1]}, \
            #{"name":"dswrf_ave",    "range":[  1, 500], "drange":[-1,1]},   \
            #{"name":"albdo_ave",    "range":[  0, 100], "drange":[-10,10]}, \
            #{"name":"dswrf_avetoa", "range":[  1,1300], "drange":[-1,1]}, \
            #{"name":"csdlf",        "range":[ 10, 500], "drange":[-1,1]}, \
            #{"name":"csdsf",        "range":[  1, 500], "drange":[-1,1]}, \
            #{"name":"csulf",        "range":[200, 600], "drange":[-1,1]}, \
            #{"name":"csulftoa",     "range":[  1, 400], "drange":[-1,1]}, \
            #{"name":"csusf",        "range":[  1, 500], "drange":[-1,1]}, \
            #{"name":"csusftoa",     "range":[  1,1300], "drange":[-1,1]}]


# RT root directory
dirRT = "/scratch2/BMC/wrfruc/jensen/socrates/model_run/socrates_rf09_13km_old_20240428_150640/2018020412"

# Which forecast hour(s)?
fcast_hr = ["000","024"]

# Map dimensions                                                                                                                                                
map_west  = 60
map_east  = 180
map_south = -70
map_north = -30

# Some map projections                                                                                                                                          
#map_proj = ccrs.LambertConformal(central_longitude=150.0, central_latitude=-40.0, standard_parallels=(-33, -45), cutoff=0)                                    
map_proj = ccrs.PlateCarree(central_longitude=150)

# For every file...
for ifile in range(0,len(fcast_hr)):
    # Get input file.
    file1  = dirRT + "/phyf" + fcast_hr[ifile] + ".nc"

    # Open datasets
    data1 = xr.open_dataset(file1,concat_characters=True,decode_cf=True)

    # For each variable...
    for ivar in range(0, len(var_dict)):
        # Create output file.
        fileOUT = "ufs."+var_dict[ivar]["name"]+"."+fcast_hr[ifile] +".png"
        
        # Determine plot levels.
        plot_levels = np.linspace(var_dict[ivar]["range"][0],  var_dict[ivar]["range"][1],  nlev)
        
        # Create temporary plot variable for ease.
        var_name = var_dict[ivar]["name"]
        var_data = data1[var_name]
        varPlt = var_data[0,:,:].values
        lon    = data1.grid_xt.values
        lat    = data1.grid_yt.values
        long_name = var_data.attrs.get("long_name", var_name)
        units = var_data.attrs.get("units", "")
        # Set up figure
        fig = plt.figure(figsize=(12,8))
        ax = fig.add_subplot(1, 1, 1, projection= map_proj)
        ax.set_extent([map_west, map_east, map_south, map_north])

        #land
        land_10m = cfeature.NaturalEarthFeature('physical', 'land', '10m', edgecolor='k')

        # ocean
        ocean_10m = cfeature.NaturalEarthFeature('physical', 'ocean', '10m, edgecolor='k')

        # ocean                                                                                                                                                         
        lakes_10m = cfeature.NaturalEarthFeature('physical', 'lakes', '10m', edgecolor='k')

        # Countries                                                                                                                                                     
        c_10m = cfeature.NaturalEarthFeature('cultural', 'admin_0_countries', '10m', edgecolor='k')

        ax.add_feature(land_10m,zorder=1)
        ax.add_feature(ocean_10m,zorder=2)
        ax.add_feature(lakes_10m,zorder=3)
        ax.add_feature(c_10m,zorder=4)

        # Make contour contourf
        contourf_plot = ax.contourf(lon, lat, varPlt, levels=plot_levels, cmap=cmap_seq)
        cbar = plt.colorbar(contourf_plot, ax=ax, orientation='vertical')
        cbar.set_label(f"{long_name}" units)
        ax.set_title(f"{long_name} at {fcast_hr[ifile]} hours")
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        # Save
        print(fileOUT)
        fig.savefig(fileOUT)
        plt.show()
        plt.close(fig)
