import sys
import os
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.feature import ShapelyFeature, NaturalEarthFeature
from netCDF4 import Dataset
import numpy as np

flight_data_path = '/scratch1/BMC/gmtb/Dustin.Swales/Lapenta/Lily/data/OBS/flight_data/RF09H.20180204.225000_070500.PNI.nc'
fdir = '/scratch1/BMC/gmtb/Dustin.Swales/Lapenta/Lily/data/OBS/soundings/'
#flight_data_path = 'flight_data/RF09H.20180204.225000_070500.PNI.nc' #used for running locally
#fdir = 'radiosonde_data/' #used for running locally
filenames = ['SOCRATES_HighRes_20180204_1115_Melbourne.txt',
             'SOCRATES_HighRes_20180204_1219_ISS3.txt',
             'SOCRATES_HighRes_20180204_1715_Hobart.txt',
             'SOCRATES_HighRes_20180204_2141_Invercargill.txt',
             'SOCRATES_HighRes_20180204_2315_Casey.txt',
             'SOCRATES_HighRes_20180204_2316_Hobart.txt',
             'SOCRATES_HighRes_20180204_1120_Hobart.txt',
             'SOCRATES_HighRes_20180204_1600_ISS3.txt',  
             'SOCRATES_HighRes_20180204_1907_ISS3.txt',
             'SOCRATES_HighRes_20180204_2207_ISS3.txt',
             'SOCRATES_HighRes_20180204_2315_Melbourne.txt',
             'SOCRATES_HighRes_20180204_2328_Macquarie.txt'
]
header_lines_ignore = 12
data_start_index= 15

def process_file(filename):
    filepath = os.path.join(fdir,filename)
    with open(filepath, 'r') as readfile:
        lines = readfile.readlines()
    data = {}
    var_names = []
    for index, line in enumerate(lines):
        if index < header_lines_ignore:
            continue
        elif  index == header_lines_ignore:
            var_names = line.strip().split()
            # Set up place to store data
            data = {var: [] for var in var_names}
        elif index >= data_start_index:
            if '9999' not in line:
                entries = line.strip().split()
                if len(entries) == len(var_names):
                    for ind, entry in enumerate(entries):
                        varid = var_names[ind]
                        try:
                            data[varid].append(float(entry))
                        except ValueError:
                            print(f"skipping non-numeric value in {varid}: {entry}")
    if "Lon" in data and "Lat" in data:
        corrected_lon = [lon for lon in data["Lon"] if lon != 9999]
        lat = [lat for lat in data["Lat"] if lat != 9999]
        if corrected_lon and lat:
            return corrected_lon, lat
    return None, None

#colormap= plt.colormaps#['tab10']
# Map dimensions                                                                                                                                                
map_west  = 60
map_east  = 180
map_south = -70
map_north = -30

# Some map projections                                                                                                                                          
#map_proj = ccrs.LambertConformal(central_longitude=150.0, central_latitude=-40.0, standard_parallels=(-33, -45), cutoff=0)                                    
map_proj = ccrs.PlateCarree(central_longitude=150)

# Set up the figure and axes                                                                                                                                    
fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(1, 1, 1, projection=map_proj)
ax.set_extent([map_west, map_east, map_south, map_north])

# Add features to map                                                                                                                                           
# Land                                                                                                                                                          
land_10m = cfeature.NaturalEarthFeature('physical', 'land', '10m',
                                        edgecolor='k', facecolor='lightgrey', alpha=0.4)

# Ocean                                                                                                                                                         
ocean_10m = cfeature.NaturalEarthFeature('physical', 'ocean', '10m',
                                         edgecolor='face', facecolor='C0', alpha=0.1)

# Lakes                                                                                                                                                         
lakes_10m = cfeature.NaturalEarthFeature('physical', 'lakes', '10m',
                                         edgecolor='face', facecolor='C0', alpha=0.6)

# Countries                                                                                                                                                     
c_10m = cfeature.NaturalEarthFeature('cultural', 'admin_0_countries', '10m',
                                     edgecolor='k', facecolor='none')

ax.add_feature(land_10m,zorder=1)
ax.add_feature(ocean_10m,zorder=2)
ax.add_feature(lakes_10m,zorder=3)
ax.add_feature(c_10m,zorder=4)

# Set colors to use in image.
#colors = cm.rainbow(np.linspace(0, 1, len(filenames)))
colors = cm.get_cmap('tab20', len(filenames))
# Add some aircraft observations
flight_data = Dataset(flight_data_path)
flight_path, = ax.plot(flight_data.variables['LON'][:], flight_data.variables['LAT'][:], transform=ccrs.PlateCarree(), zorder=9, label='Flight Path', color='blue')
legend_elements = [(flight_path, 'Flight path')]
for i, fname in enumerate(filenames):
    # Pull out site name from filename.
    time_start = fname.find("20180204_") + len("20180204_") 
    launch_time = fname[time_start:time_start + 4] 
    site_name_start = time_start + 5
    site_name_end = fname.rfind('.txt')
    siteName = fname[site_name_start:site_name_end]
    corrected_lon, lat = process_file(fname)
    if corrected_lon and lat:
        ax.plot(corrected_lon, lat, transform=ccrs.PlateCarree(),zorder=9,color=colors(i))
        scatter = ax.scatter(corrected_lon[0],lat[0],transform=ccrs.PlateCarree(),zorder=9, color=colors(i),s=25)
        launch_time_formatted = f'{launch_time[:2]}:{launch_time[2:]} UTC'
        legend_elements.append((scatter, f'{siteName} launch at {launch_time_formatted}'))
ax.set_title("Radiosonde and Flight Launch Points and Paths")
legend_labels = [element[1] for element in legend_elements]
legend_handles = [element[0] for element in legend_elements]
ax.legend(legend_handles, legend_labels, loc='upper left')
plt.show()
# Save figures                                                                                                                                                  
# Larger dpi is higher resolution (try dpi=300 if too fuzzy)                                                                                                    
fig.savefig('socrates_flight&radiosonde_map.png', dpi=300, bbox_inches='tight')
