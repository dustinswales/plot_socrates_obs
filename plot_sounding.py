import sys
import matplotlib.pyplot as plt
import numpy as np

fdir = '/Users/lilyjohnston/socrates/plot_socrates_obs'
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
            for ind, entry in enumerate(line.strip().split()):
                varid = var_names[ind]
                data[varid].append(float(entry))
            
readfile.close()

# We read the data into a python dictionary called data. The keys for this dictionary are stored in var_names
print(var_names)

#print(data['Temp'])
#print(data['Alt'])

# Here is where you set up plotting
figure=plt.figure(figsize=(16,16))
plt.plot(data["Temp"][:],data["Alt"], color='blue')
plt.title("Temperature Profile")
plt.ylabel('Altitude (m)')
plt.xlabel('Temperature (C)')
plt.savefig('fig3.png')
plt.show()



