import os
import numpy as np
from netCDF4 import Dataset

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx],idx

def read_UFS(lon, lat, lev, time, flight_time_start, flight_time_end, ufs_data_path, vars2plt, debug=False):

    nobs = len(lon)
    if debug: nobs = 40
    
    # Get UFS files in provided directory.
    files = os.listdir(ufs_data_path)
    files = sorted(files)
    files_atm = []
    files_sfc = []
    for file_ in files:
        if file_.startswith('atmf'): files_atm.append(file_)
        if file_.startswith('sfcf'): files_sfc.append(file_)
    # end for
    files_atm = sorted(files_atm)
    files_sfc = sorted(files_sfc)

    # Check that we have correct number of files, otherwise quit.
    if (len(files_atm) != len(files_sfc)):
        print("ERROR: Number of 2D and 3D UFS files do not match. Quitting")
        exit()
    # end if

    # Get the time information from the UFS experiment.
    # a) atmf*.nc files (3d)
    ufs_atm_time = {"year":[],"month":[],"day":[],"hour":[],"minute":[],"second":[],"time_iso":[]}
    for file_atm in files_atm:
        data = Dataset(ufs_data_path+"/"+file_atm)
        time_iso = data["time_iso"][:][0]
        ufs_atm_time["year"].append(int(time_iso[0:4]))
        ufs_atm_time["month"].append(int(time_iso[6:7]))
        ufs_atm_time["day"].append(int(time_iso[8:10]))
        ufs_atm_time["hour"].append(int(time_iso[11:13]))
        ufs_atm_time["minute"].append(int(time_iso[14:16]))
        ufs_atm_time["second"].append(int(time_iso[17:18]))
        ufs_atm_time["time_iso"].append(time_iso)
    # end for
    # b) sfcf*.nc files (2d)
    ufs_sfc_time = {"year":[],"month":[],"day":[],"hour":[],"minute":[],"second":[],"time_iso":[]}
    for file_sfc in files_sfc:
        data = Dataset(ufs_data_path+"/"+file_sfc)
        time_iso = data["time_iso"][:][0]
        ufs_sfc_time["year"].append(int(time_iso[0:4]))
        ufs_sfc_time["month"].append(int(time_iso[6:7]))
        ufs_sfc_time["day"].append(int(time_iso[8:10]))
        ufs_sfc_time["hour"].append(int(time_iso[11:13]))
        ufs_sfc_time["minute"].append(int(time_iso[14:16]))
        ufs_sfc_time["second"].append(int(time_iso[17:18]))
        ufs_sfc_time["time_iso"].append(time_iso)
    # end for

    # Check that the times match, otherwise quit.
    for ifile in range(0,len(files_sfc)):
        if not (ufs_sfc_time["time_iso"][ifile] == ufs_atm_time["time_iso"][ifile]):
            print("ERROR: Times in UFS atmosphere files (atmf.*nc) is inconsistent with surface files (sfcf*.nc). Quitting")
            exit()
        # end if
    # end for

    # Grab UFS grid description.
    data = Dataset(ufs_data_path+"/"+files_sfc[0])
    ufs_lon = data["lon"][:,:]
    ufs_lat = data["lat"][:,:]
    lonx    = data["grid_xt"][:]
    laty    = data["grid_yt"][:]
    levz    = data["pfull"][:]
    
    # Find the nearest grid point for each observation, use closet UFS grid point
    nearest = {"xi":[], "yi":[], "zi":[]}
    for ix in range(0,nobs):
        #
        lon_, loni = find_nearest(lonx,lon[ix])
        lat_, lati = find_nearest(laty,lat[ix])
        lev_, levi = find_nearest(levz,lev[ix])
        nearest["xi"].append(loni)
        nearest["yi"].append(lati)
        nearest["zi"].append(levi)
    # end for

    # Initialize output dictionary
    dataUFS={}
    for var2plt in vars2plt:
        dataUFS[var2plt]=[]
    # end for

    # Extract data
    tempVar = np.zeros(len(files_atm))
    for iobs in range(0,nobs):
        for var2plt in vars2plt:
            for count,file_atm in enumerate(files_atm):
                data = Dataset(ufs_data_path+"/"+file_atm)
                tempVar[count] = data[var2plt][0,nearest["zi"][iobs],nearest["yi"][iobs],nearest["xi"][iobs]]
            # end for
            # Interpolate tempVar in time to tempVari (*TO DO*)
            tempVari = tempVar[0]
            # Store
            dataUFS[var2plt].append(tempVari)
        # end for
    # end for
    
    return dataUFS

# end def

########################################################################################
#
########################################################################################    

# Get flight path location/level/times
flight_data_path = '/scratch1/BMC/gmtb/Dustin.Swales/Lapenta/Lily/data/OBS/flight_data'
flight_data_file = 'RF09H.20180204.225000_070500.PNI.nc'
ufs_data_path    = '/scratch1/BMC/gmtb/Dustin.Swales/Lapenta/Lily/data/UFS/control_c48'
vars2plt         = ['tmp','ugrd','vgrd','spfh','snmr','rwmr']

# Parse filename for flight start/end times.
flight_start_year   = int(flight_data_file[6:10])
flight_start_month  = int(flight_data_file[10:12])
flight_start_day    = int(flight_data_file[12:14])
flight_start_hour   = int(flight_data_file[15:17])
flight_start_minute = int(flight_data_file[17:19])
flight_start_second = int(flight_data_file[19:21])
flight_end_hour     = int(flight_data_file[22:24])
flight_end_minute   = int(flight_data_file[24:26])
flight_end_second   = int(flight_data_file[26:28])
flight_end_year     = flight_start_year
flight_end_month    = flight_start_month
flight_end_day      = flight_start_day
if (flight_end_hour < flight_start_hour):
    flight_end_day = flight_end_day +  1
# end if

# Store in dictionary.
flight_time_start = {"year":   flight_start_year,   "month":  flight_start_month,
                     "day":    flight_start_day,    "hour":   flight_start_hour,
                     "minute": flight_start_minute, "second": flight_start_second}
flight_time_end   = {"year":   flight_end_year,     "month":  flight_end_month,
                     "day":    flight_end_day,      "hour":   flight_end_hour,
                     "minute": flight_end_minute,   "second": flight_end_second}


# Pull out fields from flight data.
flight_data = Dataset(flight_data_path+'/'+flight_data_file)
lons  = flight_data.variables['LON'][:]
lats  = flight_data.variables['LAT'][:]
levs  = flight_data.variables['PSX'][:,1]
times = flight_data.variables['Time'][:]

#
dataUFS = read_UFS(lons, lats, levs, times, flight_time_start, flight_time_end, ufs_data_path, vars2plt)

