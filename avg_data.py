import sys
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import pandas as pd
import numpy as np

print(f"Python version: {sys.version}")

flight_data_path = '/scratch2/BMC/wrfruc/jensen/socrates/observations/aircraft_state_obs/RF09H.20180204.225000_070500.PNI.nc'

# Add some aircraft observations
flight_data = Dataset(flight_data_path)

# Create dataframe
d = {'Time': flight_data.variables['Time'][:], 'Lon': flight_data.variables['LON'][:], 'LWC': np.mean(flight_data.variables['PLWCC'][:], axis=1),'T':np.mean(flight_data.variables['THETA'][:], axis=1)}
df = pd.DataFrame(data=d)

# Time variable is seconds since 2018-02-04 00:00:00 +0000"
start_time = pd.to_datetime('2018-02-04 00:00:00', format='%Y-%m-%d %H:%M:%S')

df['start_time'] = start_time
df['current_time'] = df['start_time'] + pd.to_timedelta(df['Time'], unit='s')

print(df)

# Assume aircraft speed of 100 m/s -> 13000 meter grid spacing -> time average: 130 seconds (let's round to 2 minutes)
average_time_sec = 120.

# Get the first and last observation time
first_obs_time = df.iloc[0]['current_time']
last_obs_time = df.iloc[-1]['current_time']
print(f"first observation time: {first_obs_time}, last observation time: {last_obs_time}")

avg_lwc = []
avg_t=[]
middle_time = []

iterate_time0 = first_obs_time
iterate_time1 = iterate_time0 + pd.to_timedelta(average_time_sec, unit='s')

# iterate over the dataframe in 2-minute intervals
while iterate_time0 < last_obs_time:
    # print(iterate_time0, iterate_time1)

    middle_time.append(iterate_time0 + pd.to_timedelta(average_time_sec/2., unit='s'))

    # Subset the dataframe to include our time window
    df_tmp = df.loc[(df['current_time'] >= iterate_time0) & (df['current_time'] < iterate_time1)]
    avg_t.append(df_tmp['T'].mean())
    avg_lwc.append(df_tmp['LWC'].mean())
    
    iterate_time0 += pd.to_timedelta(average_time_sec, unit='s')
    iterate_time1 = iterate_time0 + pd.to_timedelta(average_time_sec, unit='s')

df_avg = pd.DataFrame({'Time': middle_time, 'LWC_Average': avg_lwc, 'T_Average':avg_t})
print(df_avg)
# Plotting
fig, ax = plt.subplots(2,1, figsize=(12,4))
ax[0,0].plot(df['current_time'], df['LWC'], label='1-second data')
ax[0,0].set_xlabel('Time [UTC]')
ax[0,0].set_ylabel(r'LWC [g m$^{-3}$]')
ax[0,0].set_ylim((0,2))
ax[0,0].scatter(df_avg['Time'], df_avg['LWC_Average'], label='2-minute data', color='C1', s=10, zorder=2)
ax.legend()
fig.savefig('avg_data.pdf', dpi=50, bbox_inches='tight')
plt.show()
