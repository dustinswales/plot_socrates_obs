import sys

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.feature import ShapelyFeature, NaturalEarthFeature
from netCDF4 import Dataset

print(f"Python version: {sys.version}")
flight_data_path = '/Users/lilyjohnston/socrates/plot_socrates_obs/flight_data/RF09H.20180204.225000_070500.PNI.nc'

fdir = '/Users/lilyjohnston/socrates/plot_socrates_obs/radiosonde_data'
fname = 'SOCRATES_HighRes_20180205_2330.txt'

header_lines_ignore = 12
data_start_index= 15

readfile = open(fdir + '/' + fname, 'r')
lines = readfile.readlines()

for index, line in enumerate(lines):
	if index < header_lines_ignore:
		print(f"Ignoring header line: {line.strip()}")
	else:
		# This is the line that has variable name information
		if index == header_lines_ignore:
			var_names = line.strip().split()
			# Set up place to store data
			data = {}
			for var in var_names:
				data[var] = []
			print(f"Variables names: {var_names}")
        # Continue reading lines
	if index < data_start_index:
		print(f"Ignoring header line: {line.strip()}")
	else:
		# This is the first line with actual data
		if index == data_start_index:
			print(f"Sample data line from first entry: {line.strip().split()}")
		# Add data to dictonary
		if '9999' in line:
			print('found bunk point')
		else:
			for ind, entry in enumerate(line.strip().split()):
				varid = var_names[ind]
				data[varid].append(float(entry))
readfile.close()

corrected_lon=[]
for lon in data["Lon"]:
	corrected_lon.append(lon)
print(corrected_lon)
# We read the data into a python dictionary called data. The keys for this dictionary are stored in var_names
print(var_names)

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


# Add some aircraft observations
flight_data = Dataset(flight_data_path)
ax.plot(flight_data.variables['LON'][:], flight_data.variables['LAT'][:], transform=ccrs.PlateCarree(), zorder=9, label='Flight Path', color='blue')
ax.plot(corrected_lon,data["Lat"],transform=ccrs.PlateCarree(),zorder=9,label='Radiosonde Path', color='g')
ax.scatter(corrected_lon[0],data["Lat"][0],transform=ccrs.PlateCarree(),zorder=9,label='Launch Point', color='r',s=10)
ax.legend()
plt.show()
# Save figures                                                                                                                                                  
# Larger dpi is higher resolution (try dpi=300 if too fuzzy)                                                                                                    
fig.savefig('socrates_flight&radiosonde_map.pdf', dpi=50, bbox_inches='tight')
