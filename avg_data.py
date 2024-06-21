import sys
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import pandas as pd
import numpy as np

print(f"Python version: {sys.version}")

flight_data_path = '/scratch2/BMC/wrfruc/jensen/socrates/observations/aircraft_state_obs/RF09H.20180204.225000_070500.PNI.nc'

# Add some aircraft observations
flight_data = Dataset(flight_data_path, 'r')
print('Variables in NetCDF file:')
for variable_name in flight_data.variables:
    variable=flight_data.variables[variable_name]
    long_name=variable.getncattr('long_name') if 'long_name' in variable.ncattrs() else 'No long_name attribute'
    print(f"{variable_name}: {long_name}")
# Create dataframe
d = {'Time': flight_data.variables['Time'][:], 'Lon': flight_data.variables['LON'][:], 'LWC': np.mean(flight_data.variables['PLWCC'][:], axis=1),'T':np.mean(flight_data.variables['THETA'][:], axis=1),'P':np.mean(flight_data.variables['PALT'][:], axis=1),'GPS_Alt':np.mean(flight_data.variables['GGALT'][:]) ,'LAT':np.mean(flight_data.variables['LATC'][:], axis=1),'LON':np.mean(flight_data.variables['LONC'][:], axis=1),'T':np.mean(flight_data.variables['THETA'][:], axis=1),'U':np.mean(flight_data.variables['UI'][:], axis=1),'V':np.mean(flight_data.variables['VI'][:], axis=1)}
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
min_lwc = []
max_lwc = []
avg_t=[]
min_t = []
max_t =	[]
avg_p=[]
min_p =	[]
max_p = []
avg_alt=[]
min_alt = []
max_alt = []
avg_lat=[]
min_lat = []
max_lat = []
avg_lon=[]
min_lon = []
max_lon = []
avg_u=[]
min_u =	[]
max_u = []
avg_v=[]
min_v =	[]
max_v = []
middle_time = []

iterate_time0 = first_obs_time
iterate_time1 = iterate_time0 + pd.to_timedelta(average_time_sec, unit='s')

# iterate over the dataframe in 2-minute intervals
while iterate_time0 < last_obs_time:
    # print(iterate_time0, iterate_time1)

    middle_time.append(iterate_time0 + pd.to_timedelta(average_time_sec/2., unit='s'))

    # Subset the dataframe to include our time window
    df_tmp = df.loc[(df['current_time'] >= iterate_time0) & (df['current_time'] < iterate_time1)]
    avg_lwc.append(df_tmp['LWC'].mean())
    min_lwc.append(df_tmp['LWC'].min())
    max_lwc.append(df_tmp['LWC'].max())
    avg_t.append(df_tmp['T'].mean())
    min_t.append(df_tmp['T'].min())
    max_t.append(df_tmp['T'].max())
    avg_p.append(df_tmp['P'].mean())
    min_p.append(df_tmp['P'].min())
    max_p.append(df_tmp['P'].max())
    avg_alt.append(df_tmp['GPS_Alt'].mean())
    min_alt.append(df_tmp['GPS_Alt'].min())
    max_alt.append(df_tmp['GPS_Alt'].max())
    avg_lat.append(df_tmp['LAT'].mean())
    min_lat.append(df_tmp['LAT'].min())
    max_lat.append(df_tmp['LAT'].max())
    avg_lon.append(df_tmp['LON'].mean())
    min_lon.append(df_tmp['LON'].min())
    max_lon.append(df_tmp['LON'].max())
    avg_u.append(df_tmp['U'].mean())
    min_u.append(df_tmp['U'].min())
    max_u.append(df_tmp['U'].max())
    avg_v.append(df_tmp['V'].mean())
    min_v.append(df_tmp['V'].min())
    max_v.append(df_tmp['V'].max())
    iterate_time0 += pd.to_timedelta(average_time_sec, unit='s')
    iterate_time1 = iterate_time0 + pd.to_timedelta(average_time_sec, unit='s')

df_avg = pd.DataFrame({'Time': middle_time, 'LWC_Average': avg_lwc, 'LWC_Min': min_lwc, 'LWC_Max': max_lwc, 'T_Average':avg_t,'T_Min': min_t, 'T_Max': max_t,'P_Average':avg_p,'P_Min': min_p, 'P_Max': max_p,'Alt_Average':avg_alt,'Alt_Min': min_alt, 'Alt_Max': max_alt,'Lat_Average':avg_lat,'Lat_Min': min_lat, 'Lat_Max': max_lat,'Lon_Average':avg_lon,'Lon_Min': min_lon, 'Lon_Max': max_lon,'U_Average':avg_u,'U_Min': min_u, 'U_Max': max_u,'V_Average':avg_v,'V_Min': min_v, 'V_Max': max_v})
print(df_avg)

start_time_limit = start_time + pd.to_timedelta(95000, unit='s')
end_time_limit = start_time + pd.to_timedelta(105000, unit='s')
# Plotting
fig, ax = plt.subplots(2,4, figsize=(12,4))
#plotting LWC
ax[0,0].plot(df['current_time'], df['LWC'], label='1-second data')
ax[0,0].set_xlabel('Time [UTC]')
ax[0,0].set_ylabel(r'LWC [g m$^{-3}$]')
ax[0,0].set_ylim((0,2))
ax[0,0].scatter(df_avg['Time'], df_avg['LWC_Average'], label='2-minute data average', color='C1', s=10, zorder=2)
ax[0,0].scatter(df_avg['Time'], df_avg['LWC_Min'], label='2-minute data maximum', color='k', s=10, zorder=3)
ax[0,0].scatter(df_avg['Time'], df_avg['LWC_Max'], label='2-minute data minimum', color='g', s=10, zorder=4)
ax[0,0].set_xlim(start_time_limit,end_time_limit)
ax[0,0].set_title('Liquid Water Content')
ax[0,0].legend(fontsize='xx-small',loc='upper left')

#Plotting temperature
ax[0,1].plot(df['current_time'], df['T'], label='1-second data')
ax[0,1].set_xlabel('Time [UTC]')
ax[0,1].set_ylabel(r'T [deg C]')
ax[0,1].scatter(df_avg['Time'], df_avg['T_Average'], label='2-minute data average', color='C1', s=10, zorder=2)
ax[0,1].scatter(df_avg['Time'], df_avg['T_Min'], label='2-minute data maximum', color='k', s=10, zorder=3)
ax[0,1].scatter(df_avg['Time'], df_avg['T_Max'], label='2-minute data minimum', color='g', s=10, zorder=4)
ax[0,1].set_xlim(start_time_limit,end_time_limit)
ax[0,1].set_title('Potential Temperature')
ax[0,1].legend(fontsize='xx-small',loc='upper right')

#plotting pressure
ax[0,2].plot(df['current_time'], df['P'], label='1-second data')
ax[0,2].set_xlabel('Time [UTC]')
ax[0,2].set_ylabel(r'Pressure Altitude (m)')
ax[0,2].scatter(df_avg['Time'], df_avg['P_Average'], label='2-minute data average', color='C1', s=10, zorder=2)
ax[0,2].scatter(df_avg['Time'], df_avg['P_Min'], label='2-minute data maximum', color='k', s=10, zorder=3)
ax[0,2].scatter(df_avg['Time'], df_avg['P_Max'], label='2-minute data minimum', color='g', s=10, zorder=4)
ax[0,2].set_xlim(start_time_limit,end_time_limit)
ax[0,2].set_title('Pressure Altitude')
ax[0,2].legend(fontsize='xx-small',loc='lower left',bbox_to_anchor=(0.1,0))

#plotting alt
ax[0,3].plot(df['current_time'], df['GPS_Alt'], label='1-second data')
ax[0,3].set_xlabel('Time [UTC]')
ax[0,3].set_ylabel(r'GPS Altitude (m)')
ax[0,3].scatter(df_avg['Time'], df_avg['Alt_Average'], label='2-minute data average', color='C1', s=10, zorder=2)
ax[0,3].scatter(df_avg['Time'], df_avg['Alt_Min'], label='2-minute data maximum', color='k', s=10, zorder=3)
ax[0,3].scatter(df_avg['Time'], df_avg['Alt_Max'], label='2-minute data minimum', color='g', s=10, zorder=4)
ax[0,3].set_xlim(start_time_limit,end_time_limit)
ax[0,3].set_title('GPS Altitude')
y_min,y_max= df['GPS_Alt'].min(),df['GPS_Alt'].max()
if y_min == y_max:
    buffer = 0.1 * y_max if y_max !=0 else 0.1
    ax[0,3].set_ylim(y_min - buffer, y_max + buffer)
else:
    buffer = 0.01 * (y_max - y_min)
    ax[0,3].set_ylim(y_min - buffer, y_max - buffer)

ax[0,3].set_ylim(4374,4376)
ax[0,3].legend(fontsize='xx-small',loc='lower right')

#plotting lat
ax[1,0].plot(df['current_time'], df['LAT'], label='1-second data')
ax[1,0].set_xlabel('Time [UTC]')
ax[1,0].set_ylabel(r'Latitude')
ax[1,0].scatter(df_avg['Time'], df_avg['Lat_Average'], label='2-minute data average', color='C1', s=10, zorder=2)
ax[1,0].scatter(df_avg['Time'], df_avg['Lat_Min'], label='2-minute data maximum', color='k', s=10, zorder=3)
ax[1,0].scatter(df_avg['Time'], df_avg['Lat_Max'], label='2-minute data minimum', color='g', s=10, zorder=4)
ax[1,0].set_xlim(start_time_limit,end_time_limit)
ax[1,0].set_title('Latitude')
ax[1,0].legend(fontsize='xx-small',loc='upper center')

#plotting lon
ax[1,1].plot(df['current_time'], df['LON'], label='1-second data')
ax[1,1].set_xlabel('Time [UTC]')
ax[1,1].set_ylabel(r'Longitude')
ax[1,1].scatter(df_avg['Time'], df_avg['Lon_Average'], label='2-minute data average', color='C1', s=10, zorder=2)
ax[1,1].scatter(df_avg['Time'], df_avg['Lon_Min'], label='2-minute data maximum', color='k', s=10, zorder=3)
ax[1,1].scatter(df_avg['Time'], df_avg['Lon_Max'], label='2-minute data minimum', color='g', s=10, zorder=4)
ax[1,1].set_title('Longitude')
ax[1,1].set_xlim(start_time_limit,end_time_limit)
ax[1,1].legend(fontsize='xx-small',loc='lower center')

#plotting u
ax[1,2].plot(df['current_time'], df['U'], label='1-second data')
ax[1,2].set_xlabel('Time [UTC]')
ax[1,2].set_ylabel(r'U (m/s)')
ax[1,2].scatter(df_avg['Time'], df_avg['U_Average'], label='2-minute data average', color='C1', s=10, zorder=2)
ax[1,2].scatter(df_avg['Time'], df_avg['U_Min'], label='2-minute data maximum', color='k', s=10, zorder=3)
ax[1,2].scatter(df_avg['Time'], df_avg['U_Max'], label='2-minute data minimum', color='g', s=10, zorder=4)
ax[1,2].set_xlim(start_time_limit,end_time_limit)
ax[1,2].set_title('U (m/s)')
ax[1,2].legend(fontsize='xx-small',loc='lower center')

#plotting v
ax[1,3].plot(df['current_time'], df['V'], label='1-second data')
ax[1,3].set_xlabel('Time [UTC]')
ax[1,3].set_ylabel(r'V (m/s)')
ax[1,3].scatter(df_avg['Time'], df_avg['V_Average'], label='2-minute data average', color='C1', s=10, zorder=2)
ax[1,3].scatter(df_avg['Time'], df_avg['V_Min'], label='2-minute data maximum', color='k', s=10, zorder=3)
ax[1,3].scatter(df_avg['Time'], df_avg['V_Max'], label='2-minute data minimum', color='g', s=10, zorder=4)
ax[1,3].set_title('V (m/s)')
ax[1,3].set_xlim(start_time_limit,end_time_limit)
ax[1,3].legend(fontsize='xx-small',loc='lower left',bbox_to_anchor=(0.2,0))

plt.tight_layout()
fig.savefig('avg_plots.pdf', dpi=50, bbox_inches='tight')
plt.show()
