#!/usr/bin/env python

###############################################################################
#
# This script compares SCM output from two simulations.
# Defined here as Baseline (BL) and Regression Test (RT).
#
###############################################################################
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import cmocean
def plot_results(file_bl, file_rt=None, vars2plt=None):
#def plot_results(file_bl, file_rt, plot_bl, plot_rt, plot_all, debug):
    # List of SCM output fields to plot
#    vars2plot_ALL = \
#        ["pres", "pres_i","sigma","sigma_i","pres_s","qv","T","u","v","ql",   \
#         "qi","qc","qv_force_tend","T_force_tend","u_force_tend",             \
#         "v_force_tend","w_ls","u_g","v_g","dT_dt_rad_forc","h_advec_thil",   \
#         "h_advec_qt", "v_advec_thil","v_advec_qt","T_s","lhf","shf",         \
#         "tprcp_inst","tprcp_rate_inst","t2m","q2m","ustar","tsfc","tau_u",   \
#         "tau_v","upd_mf","dwn_mf","det_mf","sfc_up_lw_land","sfc_up_lw_ice", \
#         "sfc_up_lw_water","sfc_up_sw_dir_nir","sfc_up_sw_dif_nir",           \
#         "sfc_up_sw_dir_vis","sfc_up_sw_dif_vis","sfc_dwn_sw_dir_nir",        \
#         "sfc_dwn_sw_dif_nir","sfc_dwn_sw_dir_vis","sfc_dwn_sw_dif_vis",      \
#         "mp_prcp_inst","dcnv_prcp_inst","scnv_prcp_inst","pwat",             \
#         "dT_dt_lwrad","dT_dt_swrad","dT_dt_pbl","dT_dt_deepconv",            \
#         "dT_dt_shalconv","dT_dt_micro","dT_dt_ogwd","dT_dt_cgwd",            \
#         "dT_dt_phys","dT_dt_nonphys","dq_dt_pbl","dq_dt_deepconv",           \
#         "dq_dt_shalconv","dq_dt_micro","dq_dt_phys","dq_dt_nonphys",         \
#         "doz_dt_pbl","doz_dt_prodloss","doz_dt_oz","doz_dt_T","doz_dt_ovhd", \
#         "doz_dt_phys","doz_dt_nonphys","du_dt_pbl","du_dt_ogwd","dv_dt_cgwd",\
#         "du_dt_deepconv","du_dt_cgwd","du_dt_shalconv","du_dt_phys",         \
#         "du_dt_nonphys","dv_dt_pbl","dv_dt_ogwd","dv_dt_deepconv",           \
#         "dv_dt_shalconv","dv_dt_phys","dv_dt_nonphys","sfc_dwn_sw",          \
#         "sfc_up_sw","sfc_net_sw","sfc_dwn_lw","gflux","u10m","v10m","hpbl",  \
#         "tprcp_accum","ice_accum","snow_accum","graupel_accum",              \
#         "conv_prcp_accum","tprcp_rate_accum","ice_rate_accum",               \
#         "snow_rate_accum","graupel_rate_accum","conv_prcp_rate_accum",       \
#         "max_cloud_fraction","toa_total_albedo","vert_int_lwp_mp",           \
#         "vert_int_iwp_mp","vert_int_lwp_cf","vert_int_iwp_cf"]
    
#    # Smaller subset of SCM outputs to plot.
#    vars2plot_SUB = \
#        ["qv","T","u","v","ql","qi","qc","sfc_dwn_sw","sfc_up_sw",            \
#         "sfc_net_sw","sfc_dwn_lw", "u10m","v10m","hpbl","gflux",             \
#         "qv_force_tend","T_force_tend","u_force_tend","v_force_tend","w_ls", \
#         "u_g","v_g","dT_dt_rad_forc","h_advec_thil","h_advec_qt",            \
#         "v_advec_thil","v_advec_qt","T_s","lhf","shf","tprcp_inst",          \
#         "tprcp_rate_inst","t2m","q2m","ustar","tsfc","tau_u","tau_v","pwat", "max_cloud_fraction","toa_total_albedo","vert_int_lwp_mp", "vert_int_iwp_mp","vert_int_lwp_cf","vert_int_iwp_cf"]
#    vars2plot_DEBUG = \
#        ["qv","u10m"]
    vars2plot = ["u","v"]
    # Which fields to plot? (default is subset of full fields)
#    if vars2plt is None:
#        vars2plot = vars2plot_SUB
#    else:
#        vars2plot = vars2plt
    # end if

    # Only plot differences if two files provided
    plot_diff = False
    if file_rt is not None:
        plot_diff = True
    # end if
    
    # Open SCM datasets
    SCM_BL = Dataset(file_bl)
    if file_rt is not None:
        SCM_RT = Dataset(file_rt)
    # end if
    
    plot_files = []
    for var in SCM_BL.variables.keys():
        if (var in vars2plot):
            # Handle temporal axis.
            # There are 4 different dimensions in the SCM output, identified by the suffix "_dim".
            # Here the suffix is stripped and used to identify the temporal dimenesion (index 0 in netcdf file)
            timeD = SCM_BL[var].dimensions[0]
            timeD = timeD[0:len(timeD)-4]
            x1 = SCM_BL[timeD][:].squeeze()/3600. #seconds -> hours
            if file_rt is not None:
                x2 = SCM_RT[timeD][:].squeeze()/3600. #seconds - >hours
                # If temporal dimensions disagree, con't compute deltas from experiments, turn off difference plots.
                if (x1.shape != x2.shape):
                    plot_diff = False
                # end if
            # end if
            # Is this a 2D (time, x) variable? (Really 1D since x=1 in SCM)
            is2D  = False
            if (len(SCM_BL[var].dimensions)==2):
                is2D  = True
            # endif
            # one/two-dimensional variables
            if (len(SCM_BL[var].shape) != 3):
                if (is2D):
                    y1 = SCM_BL[var][:,0].squeeze()
                    if file_rt is not None:
                        y2 = SCM_RT[var][:,0].squeeze()
                    # end if
                else:
                    y1 = SCM_BL[var][:]
                    if file_rt is not None:
                        y2 = SCM_RT[var][:]
                if var == "qv":
                    y1 *= 1000 # convert kg/kg to g/kg
                    if file_rt is not None:
                        y2 *= 1000 
                    # end if
                # endif
                
                # Make figure
                if (np.size(x1) > 1):
                    fig = plt.figure(figsize=(13,10))
                    
                    # Baselines and RTs on same plot
                    if plot_diff: plt.subplot(2,1,1)
                    long_name = SCM_BL[var].description
                    #units = SCM_BL[var].units
                    units = "g/kg" if var == "qv" else SCM_BL[var].units
                    plt.title(long_name)
                    plt.plot(x1, y1,  color='blue')
                    if plot_diff: plt.plot(x2, y2,  color='black')
                    plt.ylabel(f'{long_name} ({units})')
                    plt.xlabel('Time (hours)')
                    
                    # Difference (Baseline-MRT)
                    if plot_diff:
                        plt.subplot(2,1,2)
                        plt.title("Difference (blue - black)")
                        plt.plot(x1, y1 - y2,  color='red')
                        plt.plot(x1, np.zeros(len(y1)), color='grey',linestyle='dashed')
                        plt.ylabel(f'{long_name} ({units})')
                        plt.xlabel('Time (hours)')
                    # Save figure
                    fileOUT = 'scm.' + var +'.png'
                    plt.savefig(fileOUT)
                    plot_files.append(fileOUT)
            # three-dimensional variables
            elif len(SCM_BL[var].shape) == 3:
                z1 = np.transpose(SCM_BL[var][:,:,0]).squeeze()
                if file_rt is not None:
                    z2 = np.transpose(SCM_RT[var][:,:,0]).squeeze()
                # end if

                # vertical axis
                y1 = SCM_BL["pres"][0,:].squeeze()*0.01
                if file_rt is not None:
                    y2 = SCM_RT["pres"][0,:].squeeze()*0.01
                # end if
                nlev = SCM_BL[var][:,:,0].shape[1]
                # Layer (nlev) quantities are the default, so check for case where we have an
                # interface (nlev+1) variable to plot.
                if (SCM_BL[var][:,:,0].shape[1] > len(y1)):
                    y1 = SCM_BL["pres_i"][0,:].squeeze()*0.01
                    if file_rt is not None:
                        y2 = SCM_RT["pres_i"][0,:].squeeze()*0.01
                if var == "qv":
                    z1 *= 1000
                    if file_rt is not None:
                        z2 *= 1000
                    # end if
                # endif

                # Finally, make figure.
                if (np.size(x1) > 1):
                    fig,ax = plt.subplots(figsize=(13,10))
                    if file_rt is not None:
                        fig,ax=plt.subplots(figsize=(13,10))
                    long_name = SCM_BL[var].description
                    #units = SCM_BL[var].units
                    units = "g/kg" if var == "qv" else SCM_BL[var].units
                    plt.title(long_name)
                    #plt.contourf(x1, y1, z1, 20, cmap=cmocean.cm.tempo)
                    cf=plt.contourf(x1, y1, z1, levels=np.linspace(-20,20,21), cmap=plt.get_cmap('BrBG'))
                    plt.ylim(1000,500)
                    plt.xlim(0,np.max(x1))
                    plt.ylabel('Pressure (hPa)')
                    plt.xlabel('Time (hours)')
                    cbr = plt.colorbar(cf,ax=ax, ticks=np.arange(-20,21,10))
                    cbr.set_label(f'{long_name} ({units})')
                    cf.set_clim(-20,20)
                    if file_rt is not None:
                        # SCM RTs
                        fig,ax=plt.subplots(figsize=(13,10))
                        #plt.contourf(x2, y2, z2,20, cmap=cmocean.cm.tempo)
                        cf=plt.contourf(x1, y1, z1, levels=np.linspace(-20,20,21), cmap=plt.get_cmap('BrBG')) #cmap=plt.get_cmap('BrBG')
                        plt.ylim(1000,500)
                        plt.xlim(0,np.max(x1))
                        plt.ylabel('Pressure (hPa)')
                        plt.xlabel('Time (hours)')
                        cbr = plt.colorbar(cf,ax=ax, ticks=np.arange(-20,21,10))
                        cbr.set_label('('+SCM_RT[var].units+')')
                        cf.set_clim(-20,20)
                    # end if
                    # Only plot differences if requested, and only if they are non-zero.
                    if plot_diff:
                        dz = z1-z2
                        if (np.count_nonzero(dz) > 0):
                            fig,ax=plt.subplot(figsize=(13,10))
                            plt.title("Difference (top - middle)", fontsize=8)
                            plt.contourf(x2, y2, dz,20, cmap=plt.get_cmap('BrBG'))
                            cf=plt.contourf(x1, y1, z1, levels=np.linspace(-20,20,21), cmap=cmocean.cm.tempo) 
                            plt.ylim(1000,500)
                            plt.ylabel('Pressure (hPa)')
                            plt.xlabel('Time (hours)')
                            cbr = plt.colorbar(cf,ax=ax, ticks=np.arange(-20,21,10))
                            cbr.set_label(f'{long_name} ({units})')
                            cf.set_clim(-20,20)
                        # end if (no differences exist)
                    # end if     (plot differences)
                    # Save figure
                    fileOUT = 'scm.' + var +'.png'
                    plt.savefig(fileOUT)
                    plt.close(fig)
                    plot_files.append(fileOUT)
                # end if (Have enought pts to plot?)
            # end if     (fields exist?)
        # end if         (field requested?)
    # end for            (fields in file)

    return(plot_files)



