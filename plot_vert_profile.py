import sys
import matplotlib.pyplot as plt
import numpy as np

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
               # end for
            # end if
readfile.close()

# We read the data into a python dictionary called data. The keys for this dictionary are stored in var_names
print(var_names)

#print(data['Temp'])
#print(data['Alt'])

fig,ax1 =plt.subplots() 
ax1.plot(data["Temp"][:],data["Press"],label='Temperature (°C)', color='blue')
ax1.plot(data["Dewpt"][:],data["Press"],label='Dewpoint (°C)', color='g')
ax1.set_title("Temperature & Dewpoint Profile")
ax1.set_ylabel('Pressure (mb)')
ax1.set_xlabel('Temperature (°C)')
ax1.set_yscale('log')
ax1.set_ylim(1000,10)
ax2 = ax1.twinx()
ax2.plot(data["Temp"][:],data["Alt"][:], label='Altitude (m)', visible=False)
ax2.set_ylabel('Altitude (m)')
ax1.legend()
plt.savefig('Temperature_profile.png')
fig.tight_layout()
plt.show()

# Wind speed and direction
fig,ax1 =plt.subplots()
ax1.plot(data["spd"][:],data["Press"],label='Wind Speed (m/s)', color='blue')
ax1.set_title("Wind Profile")
ax1.set_ylabel('Pressure (mb)')
ax1.set_xlabel('Wind speed (m/s)')
ax1.set_yscale('log')
ax1.set_ylim(1000,100)
ax1.set_xlim(0,50)
ax2=ax1.twiny()
ax2.plot(data["dir"][:],data["Press"], label='Wind Direction (°)', color='g')
ax2.set_xlabel('Wind Direction (°)')
ax2.set_xlim(0,360)
handles1,labels1=ax1.get_legend_handles_labels()
handles2,labels2=ax2.get_legend_handles_labels()
handles=handles1+handles2
labels=labels1+labels2
plt.legend(handles,labels)
plt.savefig('Wind_dir_spd_profile.png')
fig.tight_layout()
plt.show()

# Horizontal and verticle wind
fig,ax =plt.subplots()
ax.plot(data["Ucmp"][:],data["Press"],label='U Wind (m/s)', color='blue')
ax.plot(data["Vcmp"][:],data["Press"],label='V Wind (m/s)', color='g')
ax.axvline(x=0,color='r',linestyle='--')
ax.set_title("Wind Profile")
ax.set_ylabel('Pressure (mb)')
ax.set_ylim(1000,100)
ax.set_xlabel('Wind speed (m/s)')
ax.set_xlim(-40,40)
ax.set_yscale('log')
ax.legend()
plt.savefig('u&v_profile.png')
fig.tight_layout()
plt.show()

