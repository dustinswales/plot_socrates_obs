import sys
import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset

# Observation file
dirObs  = "/Users/lilyjohnston/socrates/"
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
x = np.array(flight_data["Time"])
nx = len(x)
y = flight_data["THETA"][0,:]
ny = len(y)

# Data sanitation (TODO. Remove missing values in data)
#theta = np.zeros(shape=(nx,ny))
           
# Compute average y
theta_avg = np.nanmean(flight_data.variables["THETA"][:,:],axis=1)
thetae_avg = np.nanmean(flight_data.variables["THETAE"][:,:],axis=1)
ewx_avg = np.nanmean(flight_data.variables["EWX"][:,:],axis=1)
plwcc_avg = np.nanmean(flight_data.variables["PLWCC"][:,:],axis=1)
concn_avg = np.nanmean(flight_data.variables["CONCN"][:,:],axis=1)
rhum_avg = np.nanmean(flight_data.variables["RHUM"][:,:],axis=1)
reffd_avg = np.nanmean(flight_data.variables["REFFD_RWIO"][:,:],axis=1)
vi_avg = np.nanmean(flight_data.variables["VI"][:,:],axis=1)
ui_avg = np.nanmean(flight_data.variables["UI"][:,:],axis=1)
wi_avg = np.nanmean(flight_data.variables["WI"][:,:],axis=1)
palt_avg = np.nanmean(flight_data.variables["PALT"][:,:],axis=1)
cvcwcc_avg=np.nanmean(flight_data.variables["CVCWCC"][:,:],axis=1)
atx_avg = np.nanmean(flight_data.variables["ATX"][:,:],axis=1)
mr_avg = np.nanmean(flight_data.variables["MR"][:,:],axis=1)
vmr_avg = np.nanmean(flight_data.variables["VMR_VXL"][:,:],axis=1)
DBARD_RWIO_avg = np.nanmean(flight_data.variables["DBARD_RWIO"][:,:],axis=1)
DBARPIP_RWII_avg = np.nanmean(flight_data.variables["DBARPIP_RWII"][:,:],axis=1)
DBARU_LWII_avg = np.nanmean(flight_data.variables["DBARU_LWII"][:,:],axis=1)
fig = plt.figure(figsize=(16,16))
#Ploting THETA
plt.subplot(4,4,1)
plt.plot(flight_data.variables["Time"][:], theta_avg,  color='blue')
plt.title(flight_data["THETA"].long_name)
plt.ylabel('('+flight_data["THETA"].units+')')

#Plotting THETAE
plt.subplot(4,4,4)
plt.plot(flight_data.variables["Time"][:], theta_avg,  color='blue')
plt.title(flight_data["THETAE"].long_name)
plt.ylabel('('+flight_data["THETAE"].units+')')

#Plotting EWX 
plt.subplot(4,4,2)
plt.plot(flight_data.variables["Time"][:], ewx_avg,  color='blue')
plt.title(flight_data["EWX"].long_name)
plt.ylabel('('+flight_data["EWX"].units+')')

#Plotting PLWCC
plt.subplot(4,4,3)
plt.plot(flight_data.variables["Time"][:], plwcc_avg,  color='blue')
plt.title(flight_data["PLWCC"].long_name)
plt.ylabel('('+flight_data["PLWCC"].units+')')

#Plotting CONCN
plt.subplot(4,4,5)
plt.plot(flight_data.variables["Time"][:], concn_avg,  color='blue')
plt.title(flight_data["CONCN"].long_name)
plt.ylabel('('+flight_data["CONCN"].units+')')

#Plotting RHUM
plt.subplot(4,4,6)
plt.plot(flight_data.variables["Time"][:], rhum_avg,  color='blue')
plt.title(flight_data["RHUM"].long_name)
plt.ylabel('('+flight_data["RHUM"].units+')')

#Plotting REFF2DC
plt.subplot(4,4,7)
plt.plot(flight_data.variables["Time"][:], flight_data.variables["REFF2DC_RWOI"][:],  color='blue')
plt.title(flight_data["REFF2DC_RWOI"].long_name)
plt.ylabel('('+flight_data["REFF2DC_RWOI"].units+')')

#Plotting REFFD
plt.subplot(4,4,7)
plt.plot(flight_data.variables["Time"][:], reffd_avg,  color='blue')
plt.title(flight_data["REFFD_RWIO"].long_name)
plt.ylabel('('+flight_data["REFFD_RWIO"].units+')')

#Plotting UI
plt.subplot(4,4,8)
plt.plot(flight_data.variables["Time"][:], ui_avg,  color='blue')
plt.title(flight_data["UI"].long_name)
plt.ylabel('('+flight_data["UI"].units+')')

#Plotting VI
plt.subplot(4,4,9)
plt.plot(flight_data.variables["Time"][:], vi_avg,  color='blue')
plt.title(flight_data["VI"].long_name)
plt.ylabel('('+flight_data["VI"].units+')')

#Plotting GGALT
plt.subplot(4,4,11)
plt.plot(flight_data.variables["Time"][:], flight_data.variables["GGALT"][:],  color='blue')
plt.title(flight_data["GGALT"].long_name)
plt.ylabel('('+flight_data["GGALT"].units+')')

#Plotting PALT
plt.subplot(4,4,12)
plt.plot(flight_data.variables["Time"][:], palt_avg,  color='blue')
plt.title(flight_data["PALT"].long_name)
plt.ylabel('('+flight_data["PALT"].units+')')

#Plotting CVCWCC
plt.subplot(4,4,10)
plt.plot(flight_data.variables["Time"][:], cvcwcc_avg,  color='blue')
plt.title(flight_data["CVCWCC"].long_name)
plt.ylabel('('+flight_data["CVCWCC"].units+')')

#Plotting ATX. CVTCN,CVTP,CVTS,CVTT
plt.subplot(4,4,13)
plt.plot(flight_data.variables["Time"][:], atx_avg,label=flight_data["ATX"].long_name,  color='blue')
plt.plot(flight_data.variables["Time"][:], flight_data.variables["CVTCN"][:],label=flight_data.variables["CVTCN"].long_name, color='g')
plt.plot(flight_data.variables["Time"][:], flight_data.variables["CVTP"][:],label=flight_data.variables["CVTP"].long_name, color='k')
plt.plot(flight_data.variables["Time"][:], flight_data.variables["CVTS"][:],label=flight_data.variables["CVTS"].long_name, color='y')
plt.plot(flight_data.variables["Time"][:], flight_data.variables["CVTT"][:],label=flight_data.variables["CVTT"].long_name, color='r')
plt.title("Temperature")
plt.ylabel('('+flight_data["ATX"].units+')')
plt.legend(fontsize='xx-small',loc='upper right')
#Plotting MR and VMR
plt.subplot(4,4,14)
plt.plot(flight_data.variables["Time"][:], mr_avg,label=flight_data["MR"].long_name,  color='blue')
plt.plot(flight_data.variables["Time"][:], vmr_avg,label=flight_data["VMR_VXL"].long_name,  color='k')
plt.title("Mixing Ratio")
plt.ylabel('('+flight_data["MR"].units+')')
plt.legend(fontsize='xx-small',loc='upper right')
#Plotting Particle Sizes
plt.subplot(4,4,15)
plt.plot(flight_data.variables["Time"][:], DBARD_RWIO_avg,label=flight_data["DBARD_RWIO"].long_name,  color='blue')
plt.plot(flight_data.variables["Time"][:], DBARPIP_RWII_avg,label=flight_data["DBARPIP_RWII"].long_name,  color='k')
plt.plot(flight_data.variables["Time"][:], DBARU_LWII_avg,label=flight_data["DBARU_LWII"].long_name,  color='g')
plt.plot(flight_data.variables["Time"][:], flight_data.variables["DBAR1DC_RWOI"][:],label=flight_data.variables["DBAR1DC_RWOI"].long_name, color='r')
plt.plot(flight_data.variables["Time"][:], flight_data.variables["DBARU_CVIU"][:],label=flight_data.variables["DBARU_CVIU"].long_name, color='c')
plt.title("Particle Sizes")
plt.ylabel('('+flight_data["DBARD_RWIO"].units+')')
plt.legend(fontsize='xx-small',loc='upper right')
fig.tight_layout()
plt.savefig('/Users/lilyjohnston/Downloads/figure2.png')
plt.show()
