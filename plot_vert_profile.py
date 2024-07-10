import sys
import matplotlib.pyplot as plt
import numpy as np
import os
import netCDF4 as nc
#fdir = '/scratch1/BMC/gmtb/Dustin.Swales/Lapenta/Lily/data/OBS/soundings/'
#output_dir = '/home/Lily.Johnston/plot_socrates_obs/figures'
fdir_obs = 'radiosonde_data/'
output_dir = 'figures/'
filenames_obs = ['SOCRATES_HighRes_20180204_1115_Melbourne.txt',
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
fdir_scm = 'scm_data/'
filenames_scm = ['n001_melbourne.nc',
                 'n002_iss3.nc',
                 'n000_hobart.nc',
                 'n005_invercargill.nc',
                 'n007_casey.nc'
                 'n000_hobart.nc',
                 'n000_hobart.nc',
                 'n003_iss3.nc',
                 'n004_iss3.nc',
                 'n006_iss3.nc',
                 'n001_melbourne.nc',
                 'n008_macquarie.nc'
]
header_lines_ignore = 12
data_start_index= 15

# Constants for Clausius-Clapeyron equation
E0 = 6.11 # kPa
L_Rv = 5423 # K
T0 = 273 # K

def calculate_saturation_vapor_pressure(T):
    return E0 * np.exp(L_Rv * (1/T0 - 1/T))
def calculate_relative_humidity(qv, T, P):
    Es = calculate_saturation_vapor_pressure(T)
    E = qv * P / (0.622 + qv) # Actual vapor pressure
    return (E / Es) * 100 # Relative humidity in %
def calculate_dewpoint_temperature(RH, T):
    RH = np.clip(RH, 0, 100)
    Es = calculate_saturation_vapor_pressure(T)
    E = RH / 100 * Es
    E[E<=0] = 1e-10
    """
    for ij in range(len(E)):
        if np.any(Es[ij] > 0):
            E[ij] = E[ij]
        else:
            E[ij] = 1e-10
        # end if
    # end for
    """
    return 1 / (1/T0 - (np.log(E/E0) / L_Rv))
def calculate_wind_speed(u, v):
    return np.sqrt(u**2 + v**2)
def calculate_wind_direction(u, v):
    wdir = np.arctan2(u, v) * (180 / np.pi) # Convert from radians to degrees
    wdir = (wdir + 360) % 360 # Ensure the direction is within [0, 360) degrees
    return wdir

def process_file_obs(fdir, filename):
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

def process_file_scm(fdir, filename):
    filepath = os.path.join(fdir,filename)
    data = {}
    with nc.Dataset(filepath) as ds:
        T = ds.variables['T'][:] # Temperature in K
        P = ds.variables['pres'][:] # Pressure in kPa
        qv = ds.variables['qv_force_tend'][:] # Specific humidity
        u = ds.variables['u'][:] 
        v = ds.variables['v'][:] 
        RH = calculate_relative_humidity(qv, T, P)
        Td = calculate_dewpoint_temperature(RH, T)
        wspd = calculate_wind_speed(u, v)
        wdir = calculate_wind_direction(u, v)
        data['Temp'] = T
        data['Press'] = P
        data['qv'] = qv
        data['RH'] = RH
        data['Dewpt'] = Td
        data['Ucmp'] = u
        data['Vcmp'] = v
        data['spd'] = wspd
        data['dir'] = wdir
    return data 

def plot_data(data_obs, data_scm, filename_obs, filename_scm):
    fig,axes =plt.subplots(3,1,figsize=(10,15))
    
    #Temperature and dewpoint
    ax1 = axes[0]
    ax1.plot(data_obs["Temp"][:],data_obs["Press"],label='Temperature OBS (°C)', color='blue')
    ax1.plot(data_obs["Dewpt"][:],data_obs["Press"],label='Dewpoint OBS (°C)', color='g')
    ax1.plot(data_scm["Temp"][:],data_obs["Press"],label='Temperature SCM (°C)', color='blue', linestyle='--')
    ax1.plot(data_scm["Dewpt"][:],data_scm["Press"],label='Dewpoint SCM (°C)', color='g', linestyle='--')
    ax1.set_title(f"Temperature & Dewpoint Profile\nOBS: {filename_obs}\nSCM: {filename_scm}")
    ax1.set_ylabel('Pressure (mb)')
    ax1.set_xlabel('Temperature (°C)')
    ax1.set_yscale('log')
    ax1.set_ylim(1000,10)
    ax1.invert_yaxis()
    ax1.legend()
    #ax2 = ax1.twinx()
    #ax2.plot(data_obs["Temp"][:],data_obs["Alt"][:], label='Altitude (m)', visible=False)
    #ax2.set_ylabel('Altitude (m)')

    # Wind speed and direction
    ax2 = axes[1]
    ax2.plot(data_obs["spd"][:],data_obs["Press"],label='Wind Speed OBS (m/s)', color='blue')
    ax2.plot(data_scm["spd"][:], data_scm["Press"], label='Wind Speed SCM (m/s)', color='blue', linestyle='--')
    ax2.set_ylabel('Pressure (mb)')
    ax2.set_xlabel('Wind speed (m/s)')
    ax2.set_yscale('log')
    ax2.set_ylim(1000,100)
    ax2.set_xlim(0,50)
    ax2.invert_yaxis()
    ax3=ax2.twiny()
    ax3.plot(data_obs["dir"][:],data_obs["Press"], label='Wind Direction OBS (°)', color='g')
    ax3.plot(data_scm["dir"][:], data_scm["Press"], label='Wind Direction SCM (°)', color='g', linestyle='--')
    ax3.set_xlabel('Wind Direction (°)')
    ax3.set_xlim(0,360)
    ax2.set_title(f"Wind Speed and Direction Profile\nOBS: {filename_obs}\nSCM: {filename_scm}")
    handles1,labels1=ax2.get_legend_handles_labels()
    handles2,labels2=ax3.get_legend_handles_labels()
    handles=handles1+handles2
    labels=labels1+labels2
    ax2.legend(handles,labels)

    # Horizontal and verticle wind
    ax4 = axes[2]
    ax4.plot(data_obs["Ucmp"][:],data_obs["Press"],label='U Wind OBS (m/s)', color='blue')
    ax4.plot(data_obs["Vcmp"][:],data_obs["Press"],label='V Wind OBS (m/s)', color='g')
    ax4.plot(data_scm["Ucmp"][:], data_scm["Press"], label='U Wind SCM (m/s)', color='blue', linestyle='--')
    ax4.plot(data_scm["Vcmp"][:], data_scm["Press"], label='V Wind SCM (m/s)', color='g', linestyle='--')
    ax4.axvline(x=0,color='r',linestyle='--')
    ax4.set_title("Wind Profile")
    ax4.set_ylabel('Pressure (mb)')
    ax4.set_ylim(1000,100)
    ax4.set_xlabel('Wind speed (m/s)')
    ax4.set_xlim(-40,40)
    ax4.set_yscale('log')
    ax4.legend()

    plt.tight_layout()
    output_path = os.path.join(output_dir, f'{os.path.splitext(filename)[0]}_vs_{os.path.splittext(filename_scm)[0]}.png')
    plt.savefig(output_path)
    plt.show()
    plt.close(fig)

for filename_obs, filename_scm in zip(filenames_obs,filenames_scm):
    data_obs = process_file_obs(fdir_obs, filename_obs)
    data_scm = process_file_scm(fdir_scm, filename_scm)
    plot_data(data_obs, data_scm, filename_obs, filename_scm)

