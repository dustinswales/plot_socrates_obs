import sys
import matplotlib.pyplot as plt
import numpy as np
import os

#fdir = '/scratch1/BMC/gmtb/Dustin.Swales/Lapenta/Lily/data/OBS/soundings/'
#output_dir = '/home/Lily.Johnston/plot_socrates_obs/figures'
fdir = 'radiosonde_data/'
output_dir = 'figures/'
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
    return data

def plot_data(data, filename):
    fig,axes =plt.subplots(3,1,figsize=(10,15))
    
    #Temperature and dewpoint
    ax1 = axes[0]
    ax1.plot(data["Temp"][:],data["Press"],label='Temperature (°C)', color='blue')
    ax1.plot(data["Dewpt"][:],data["Press"],label='Dewpoint (°C)', color='g')
    ax1.set_title("Temperature & Dewpoint Profile")
    ax1.set_ylabel('Pressure (mb)')
    ax1.set_xlabel('Temperature (°C)')
    ax1.set_yscale('log')
    ax1.set_ylim(1000,10)
    ax1.invert_yaxis()
    ax1.legend()
    ax2 = ax1.twinx()
    ax2.plot(data["Temp"][:],data["Alt"][:], label='Altitude (m)', visible=False)
    ax2.set_ylabel('Altitude (m)')
    ax1.legend()

    # Wind speed and direction
    ax1 = axes[1]
    ax1.plot(data["spd"][:],data["Press"],label='Wind Speed (m/s)', color='blue')
    ax1.set_title("Wind Profile")
    ax1.set_ylabel('Pressure (mb)')
    ax1.set_xlabel('Wind speed (m/s)')
    ax1.set_yscale('log')
    ax1.set_ylim(1000,100)
    ax1.set_xlim(0,50)
    ax1.invert_yaxis()
    ax2=ax1.twiny()
    ax2.plot(data["dir"][:],data["Press"], label='Wind Direction (°)', color='g')
    ax2.set_xlabel('Wind Direction (°)')
    ax2.set_xlim(0,360)
    handles1,labels1=ax1.get_legend_handles_labels()
    handles2,labels2=ax2.get_legend_handles_labels()
    handles=handles1+handles2
    labels=labels1+labels2
    ax1.legend(handles,labels)

    # Horizontal and verticle wind
    ax = axes[2]
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

    plt.tight_layout()
    output_path = os.path.join(output_dir, f'{os.path.splitext(filename)[0]}.png')
    plt.savefig(output_path)
    plt.show()
    plt.close(fig)

for filename in filenames:
    data = process_file(filename)
    plot_data(data, filename)

