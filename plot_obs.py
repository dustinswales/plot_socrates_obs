import sys
import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset

# Observation file
dirObs  = "/scratch1/BMC/gmtb/Dustin.Swales/"
fileObs = "RF09H.20180204.225000_070500.PNI.nc"

# Add some aircraft observations
flight_data = Dataset(dirObs+fileObs)

# Loop over all fields in file, display their attributes.
count = 0
for var in flight_data.variables.keys():
    print(count,var,flight_data[var].long_name,flight_data[var].shape)
    count = count + 1
# end for

# Store some dimensions for use later.
x = flight_data["Time"]
nx = len(x)
y = flight_data["THETA"][0,:]
ny = len(y)

# Data sanitation (TODO. Remove missing values in data)
#theta = np.zeros(shape=(nx,ny))
           
# Compute average y
theta_avg = np.zeros(shape=(nx))
thetae_avg = np.zeros(shape=(nx))
for time in range(0,nx):
    y_temp = flight_data["THETA"][time,:]
    theta_avg[time] = np.sum(y_temp[~np.isnan(y_temp)])/25.
    #
    y_temp = flight_data["THETAE"][time,:]
    thetae_avg[time] = np.sum(y_temp[~np.isnan(y_temp)])/25.
# end for

fig = plt.figure(figsize=(13,10))
#
plt.subplot(2,2,1)
plt.plot(flight_data["Time"], theta_avg,  color='blue')
plt.title(flight_data["THETA"].long_name)
plt.ylabel('('+flight_data["THETA"].units+')')
#
plt.subplot(2,2,4)
plt.plot(flight_data["Time"], theta_avg,  color='blue')
plt.title(flight_data["THETAE"].long_name)
plt.ylabel('('+flight_data["THETAE"].units+')')

plt.show()

