import sys
import matplotlib.pyplot as plt
import numpy as np
import os
import netCDF4 as nc

fdir_obs = '/home/Lily.Johnston/plot_socrates_obs/radiosonde_data/'
output_dir = 'figures/'
filenames_obs = ['SOCRATES_HighRes_20180204_1115_Melbourne.txt',
             'SOCRATES_HighRes_20180204_1219_ISS3.txt',
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
fdir_scm = '/home/Lily.Johnston/plot_socrates_obs/scm_data/'
filenames_scm = ['n001_melbourne.nc',
                 'n002_iss3.nc',
                 'n005_invercargill.nc',
                 'n007_casey.nc',
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

E0 = 6.11 # kPa
L_Rv = 5423 #K
T0 = 273.15 #K

def calculate_saturation_vapor_pressure(T):
    return E0 * np.exp(L_Rv * (1/T0 - 1/(T+273.15)))
def calculate_relative_humidity(qv, T, P):
    Es = calculate_saturation_vapor_pressure(T)
    w = qv/(1-qv)
    E = w * P / (0.622 + w) # Actual vapor pressure
    return (E / Es) * 100 # Relative humidity in %
def calculate_dewpoint_temperature(RH, T):
    RH = np.clip(RH, 0, 100)
    Es = calculate_saturation_vapor_pressure(T)
    E = RH / 100 * Es
    E[E<=0] = 1e-10
    return 1 / (1/(T+273.15) - (np.log(E/E0) / L_Rv))-273.15
def calculate_wind_speed(u, v):
    wind_abs = np.sqrt(u**2 + v**2)
    return wind_abs
def calculate_wind_direction(u, v):
    wdir_trig_to = np.arctan2(u/np.sqrt(u**2 + v**2), v/np.sqrt(u**2 + v**2))
    wdir_trig_to_deg = wdir_trig_to * 180/np.pi
    wdir_from_deg = wdir_trig_to_deg + 180
    return wdir_from_deg % 360 # Ensure the direction is within [0, 360) degrees

def process_file_obs(fdir, filename):
    filepath = os.path.join(fdir,filename)
    with open(filepath, 'r') as readfile:
        lines = readfile.readlines()
    data = {}
    var_names = []
    for index, line in enumerate(lines):
        if index < header_lines_ignore-1:
            continue
        elif index == header_lines_ignore-1:
            lstamp = line[line.find(':')+1::]
        elif  index == header_lines_ignore:
            var_names = line.strip().split()
            # Set up place to store data
            data = {var: [] for var in var_names}
            # Store launch time information.
            data["launch_year"]   = int(lstamp[0:4])
            data["launch_month"]  = int(lstamp[6:8])
            data["launch_day"]    = int(lstamp[10:12])
            data["launch_hour"]   = int(lstamp[14:16])
            data["launch_minute"] = int(lstamp[17:19])
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
        T = ds.variables['T'][:]-273.15 # Temperature in C
        P = ds.variables['pres'][:]*0.01 # Pressure from Pa to hPa
        qv = ds.variables['qv'][:] # Specific humidity
        u = ds.variables['u'][:] 
        v = ds.variables['v'][:] 
        RH = calculate_relative_humidity(qv, T, P*100)
        # Td = calculate_dewpoint_temperature(RH, T)
        rv = qv / (1.0-qv) # water vapor mixing ratio (kg / kg)
        e = rv * P / 0.622 # vapor pressure (hPa)
        val1 = (17.67 / np.log(e/6.112)) - 1.0
        Td = 243.5 / val1 # Dewpoint in Celcius
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
        # Store SCM 
        fcst_time   = ds.variables['time_inst'][:]
        init_year   = ds.variables['init_year'][0]
        init_month  = ds.variables['init_month'][0]
        init_day    = ds.variables['init_day'][0]
        init_hour   = ds.variables['init_hour'][0]
        init_minute = ds.variables['init_minute'][0]
        data['fcst_time']   = fcst_time
        data['init_year']   = init_year
        data['init_month']  = init_month
        data['init_day']    = init_day
        data['init_hour']   = init_hour
        data['init_minute'] = init_minute
    return data 

def plot_data(data_obs, data_scm, filename_obs, filename_scm, scmtime2plot):
    fig,axes =plt.subplots(3,1,figsize=(10,15))

    #Temperature and dewpoint
    ax1 = axes[0]
    ax1.plot(data_obs["Temp"][:],data_obs["Press"],label='Temperature OBS (°C)', color='blue')
    ax1.plot(data_obs["Dewpt"][:],data_obs["Press"],label='Dewpoint OBS (°C)', color='g')
    ax1.plot(data_scm["Temp"][scmtime2plot,:,0],data_scm["Press"][scmtime2plot,:,0],label='Temperature SCM (°C)', color='blue', linestyle='--')
    ax1.plot(data_scm["Dewpt"][scmtime2plot,:,0],data_scm["Press"][scmtime2plot,:,0],label='Dewpoint SCM (°C)', color='g', linestyle='--')
    ax1.set_title(f"nOBS: {filename_obs}\nSCM: {filename_scm}", fontsize=16)
    ax1.set_ylabel('Pressure (mb)',fontsize=14)
    ax1.set_xlabel('Temperature (°C)',fontsize=14)
    ax1.set_yscale('log')
    ax1.set_ylim(1000,100)
    ax1.legend(fontsize=12)
    ax1.tick_params(axis='both',which='major', labelsize=12)
    # Wind speed and direction
    ax2 = axes[1]
    ax2.plot(data_obs["spd"][:],data_obs["Press"],label='Wind Speed OBS (m/s)', color='blue')
    ax2.plot(data_scm["spd"][scmtime2plot,:,0], data_scm["Press"][scmtime2plot,:,0], label='Wind Speed SCM (m/s)', color='blue', linestyle='--')
    ax2.set_ylabel('Pressure (mb)',fontsize=14)
    ax2.set_xlabel('Wind speed (m/s)',fontsize=14)
    ax2.set_yscale('log')
    ax2.set_ylim(1000,100)
    ax2.set_xlim(0,70)
    ax2.tick_params(axis='both',which='major', labelsize=12)
    #ax2.invert_yaxis()
    ax3=ax2.twiny()
    ax3.plot(data_obs["dir"][:],data_obs["Press"], label='Wind Direction OBS (°)', color='g')
    ax3.plot(data_scm["dir"][scmtime2plot,:,0], data_scm["Press"][scmtime2plot,:,0], label='Wind Direction SCM (°)', color='g', linestyle='--')
    ax3.set_xlabel('Wind Direction (°)',fontsize=14)
    ax3.set_xlim(0,360)
    ax3.tick_params(axis='both',which='major', labelsize=12)
    #ax2.set_title(f"Wind Speed and Direction Profile",fontsize=14)
    handles1,labels1=ax2.get_legend_handles_labels()
    handles2,labels2=ax3.get_legend_handles_labels()
    handles=handles1+handles2
    labels=labels1+labels2
    ax2.legend(handles,labels,fontsize=12)

    # Horizontal and verticle wind
    ax4 = axes[2]
    ax4.plot(data_obs["Ucmp"][:],data_obs["Press"],label='U Wind OBS (m/s)', color='blue')
    ax4.plot(data_obs["Vcmp"][:],data_obs["Press"],label='V Wind OBS (m/s)', color='g')
    ax4.plot(data_scm["Ucmp"][scmtime2plot,:,0], data_scm["Press"][scmtime2plot,:,0], label='U Wind SCM (m/s)', color='blue', linestyle='--')
    ax4.plot(data_scm["Vcmp"][scmtime2plot,:,0], data_scm["Press"][scmtime2plot,:,0], label='V Wind SCM (m/s)', color='g', linestyle='--')
    ax4.axvline(x=0,color='r',linestyle='--')
    #ax4.set_title("Wind Profile",fontsize=14)
    ax4.set_ylabel('Pressure (mb)',fontsize=14)
    ax4.set_ylim(1000,100)
    ax4.set_xlabel('Wind speed (m/s)',fontsize=14)
    ax4.set_xlim(-50,50)
    ax4.set_yscale('log')
    ax4.legend(fontsize=12)
    ax4.tick_params(axis='both',which='major', labelsize=12)
    plt.tight_layout()
    output_path = os.path.join(output_dir, f'{os.path.splitext(filename_obs)[0]}_vs_{os.path.splitext(filename_scm)[0]}.png')
    plt.savefig(output_path)
    plt.show()
    plt.close(fig)

for filename_obs, filename_scm in zip(filenames_obs,filenames_scm):
    # Read in SOCRATES radiosonde observations and SCN model output.
    data_obs = process_file_obs(fdir_obs, filename_obs)
    data_scm = process_file_scm(fdir_scm, filename_scm)

    # Find nearest SCM time for radiosonde launch, save index, pass to plotting routine.
    dhour = data_obs["launch_hour"]-data_scm["init_hour"]
    dmin  = data_obs["launch_minute"]-data_scm["init_minute"]
    if dhour < 0:
        itime = 0
    else:
        secintoday = dhour*3600+dmin*60
        dt = np.abs(data_scm["fcst_time"] - secintoday)
        itime = np.argmin(dt)
    # end if

    # Make plots
    plot_data(data_obs, data_scm, filename_obs, filename_scm, itime)

