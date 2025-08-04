#!/usr/bin/env python3

import os
import pandas as pd

import numpy as np
import glob
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import xarray as xr

def savefig(plot, name, dpi):
    plot.savefig(name, dpi=dpi, bbox_inches='tight')
    print('plot ist saved in : ', name)

def directory_available(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    return

def add_unit(data,var):
     
    '''Some indices do not have a unit,
    for example number of Heatwave, Hotspell'''

    if var in ['HSf','HWf']:
        data[var].attrs['units'] = 'Number'
    else:
        print('nothing to do, unit exists')
    return

def get_variable(data,var):
    '''Change the variable of absolute Temperature and unit for plotting'''
    
    if var =='TG':
        data_variable = data[var]-273.15

        data[var].attrs['units']='degree Celsius'
    else:
        data_variable = data[var]

    return data_variable


def only_land_points(data):
    '''Mask out ocean data using land-sea mask if available'''

    # Land sea mask
    lsm=xr.open_dataset('/work/ch0636/g300047/cicles/lsm_afr22_common_ohne_pur_wasser.nc')

    land_mask = lsm['sftlf'].where(lsm['sftlf'] == 1)
    data_variable= data.where(land_mask.values == 1)

    return data_variable


def plot_2diff(
        sims_rcp26,
        sims_rcp85,
        robust_rcp26,
        robust_rcp85,
        level_steps_diff, 
        color_steps_diff,
        what,
        robust,
        plotdir,
        title="",
        var="",
        robustness=False,
        westafrica=None,
        user_dpi=300,
        ):

    from cartopy import crs as ccrs
    import cartopy.feature as cf
    
    # Some graphical features:
    # set the colors:  
    levels=level_steps_diff
    colors=color_steps_diff
    hatchcolor='grey'
    plt.rcParams.update({'hatch.color': hatchcolor})

   
    font = {
        'family' : 'sans-serif',
        'weight' : 'normal',
        }

    if westafrica is True:
        height=3
    else:
        height=4.5

    # Create subplots
    fig, (ax1, ax2) = plt.subplots(1,2,figsize=(6,height), subplot_kw={'projection': ccrs.PlateCarree()}) 
      
    for ax in [ax1, ax2]:
        ax.gridlines(
            draw_labels={"bottom": "x", "left": "y"},
            dms=True,
            x_inline=False,
            y_inline=False,
            linewidth=0.5,
            )
        ax.coastlines(resolution="50m", color="black", linewidth=1)
        ax.add_feature(cf.BORDERS)
        ax.add_feature(cf.OCEAN, facecolor='#f0f0f0')
                            
        if westafrica is True:
            region='West_Africa'
            ax.set_extent([-25, 20, -0.75, 27.3])
            # Space between rows:
            fig.subplots_adjust(hspace=0.03)
            fig.subplots_adjust(wspace=0.25)
        else:
            region='Africa'
            ax.set_extent([-20, 60, -35, 35])

    # Plot data for rcp26
    for i, file in enumerate(sims_rcp26):
        print(file)
        data = xr.open_dataset(file,decode_timedelta=False)
        data_variable = data[var]
        # Mask out ocean data using land-sea mask
        data_variable = only_land_points(data_variable)

        if var !='number_of_people':
        # Select labels // Units frome metadata
        # Set title of plot
            varname=data[var].long_name
            add_unit(data,var)
            unit=data[var].units
        else:
            varname='Number of people'
            unit='Number'
        
        s = "{} {}".format(title,varname)
    
        fig.suptitle(s+": ", 
                 #fontweight='bold', 
                 x=0.5,
                 fontsize=14,
                 position=(0.5, 0.99),
                 )  
                
        im = data_variable.plot(ax=ax1,
                            levels=levels,
                            colors=colors,
                            transform=ccrs.PlateCarree(),
                            extend="both",#"neither",
                            add_colorbar=False,
                            alpha=.8,
                            )
        if robustness is True:
            robust_rcp26=file.replace(what,robust) #'_time-mean_ensemble-diff-median.nc','_ensemble-robustness.nc')
            datar = xr.open_dataset(robust_rcp26)
            datar_variable = datar[var]
            
            # Mask out ocean data using land-sea mask
            datar_variable = only_land_points(datar_variable)
            significant = xr.where(~datar_variable.isin([-1, 1, 0]), 1, 0).squeeze()
            significant = only_land_points(significant)
            significant.plot.contourf(
                        ax=ax1,
                        levels=[-.5, .5],
                        colors='none',
                        hatches=[None, None, "//", ],
                        add_colorbar=False,
                        extend='both',
                        transform=ccrs.PlateCarree()
                        )
        
        ax1.set_title(f'RCP26: {file.split("_")[5]}-{file.split("_")[6]}',fontsize=12)
    
    # Plot data for rcp85
    for i, file in enumerate(sims_rcp85):
        print('rcp85')
        print(file)
        data = xr.open_dataset(file,decode_timedelta=False)
        data_variable = data[var]
        data_variable = only_land_points(data_variable)
        im = data_variable.plot(ax=ax2,
                           levels=levels,
                           colors=colors,
                           transform=ccrs.PlateCarree(),
                           extend="both",#"neither",
                           add_colorbar=False,
                           alpha=.8,
                           )
        
        if robustness is True:
            robust_rcp85=file.replace(what,robust) #'time-mean_ensemble-diff-median.nc','ensemble-robustness.nc')
            datar = xr.open_dataset(robust_rcp85)
            datar_variable = datar[var]
            significant = xr.where(~datar_variable.isin([-1, 1, 0]), 1, 0).squeeze()
            significant = only_land_points(significant)
            significant.plot.contourf(
                    ax=ax2,
                    levels=[-.5, .5],
                    colors='none',
                    hatches=[ None,None,"//", ],
                    add_colorbar=False,
                    extend='both',
                    transform=ccrs.PlateCarree()
            )
        ax2.set_title(f'RCP85: {file.split("_")[5]}-{file.split("_")[6]}',fontsize=12)

    cbar_ax = fig.add_axes([0.15, 0.1, 0.7, 0.05])
    cbar = fig.colorbar(im, cax=cbar_ax, orientation="horizontal", label='[ '+unit+' ]')
    cbar.ax.tick_params(labelsize=10)
    cbar.set_label('[ '+unit+' ]', fontsize=10)

    name="{}/{}_diff-robust_{}_{}.png".format(plotdir, var, region, user_dpi)

    savefig(plt, "{}".format(name),user_dpi) 
    return


def plot_4diff(
        sims_rcp26,
        sims_rcp85,
        robust_rcp26,
        robust_rcp85,
        level_steps_diff, 
        color_steps_diff,
        what,
        robust,
        plotdir,
        title="",
        var="",
        robustness=None,
        westafrica=None,
        user_dpi=300,
        ):

    from cartopy import crs as ccrs
    import cartopy.feature as cf
    
    # Some graphical features:
    # set the colors:
    
    levels=level_steps_diff
    colors=color_steps_diff
    hatchcolor='grey'
    plt.rcParams.update({'hatch.color': hatchcolor})
        
    font = {
        'family' : 'sans-serif',
        'weight' : 'normal',
        }

    if westafrica is True:
        height=5.5
    else:
        height=7.5

    # Create subplots
    fig, axes = plt.subplots(
            ncols=2, nrows=2, figsize=(7,height), subplot_kw={'projection': ccrs.PlateCarree()}) 
       
    for row in axes:
        for ax in row:
            ax.gridlines(
                draw_labels={"bottom": "x", "left": "y"},
                dms=True,
                x_inline=False,
                y_inline=False,
                linewidth=0.5,
            )
            ax.coastlines(resolution="50m", color="black", linewidth=1)
            ax.add_feature(cf.BORDERS)

            #west Afrika
            #lon : -25.87 to 20 by 0.11 degrees
            #lat : -0.75 to 27.3 by 0.11 degrees
            if westafrica is True:
                region='West_Africa'
                ax.set_extent([-25, 20, -0.75, 27.3])
                # Space between rows:
                fig.subplots_adjust(hspace=0.03)
            else:
                region='Africa'
                ax.set_extent([-20, 60, -35, 35])

    # Plot data for rcp26
    for i, file in enumerate(sims_rcp26):
        print(file)
        data = xr.open_dataset(file,decode_timedelta=False)
        data_variable = data[var]
    
        # Select labels // Units frome metadata
        # Set title of plot
        varname=data[var].long_name
        add_unit(data,var)
        unit=data[var].units
        
        s = "{} {}".format(title,varname)
    
        fig.suptitle(s+": ", 
                 fontsize=14, 
                 #fontweight='bold', 
                 x=0.5,
                 position=(0.5, 0.99),
                 )  
                
        im = data_variable.plot(ax=axes[0, i],
                            levels=levels,
                            colors=colors,
                            transform=ccrs.PlateCarree(),
                            extend="both",#"neither",
                            add_colorbar=False,
                            alpha=.8,
                            )
        if robustness is True:
            robust_rcp26=file.replace(what,robust) #'time-mean_ensemble-diff-median.nc','ensemble-robustness.nc')
            datar = xr.open_dataset(robust_rcp26)
            datar_variable = datar[var]  
            significant = xr.where(~datar_variable.isin([-1, 1, 0]), 1, 0).squeeze()
            significant.plot.contourf(
                        ax=axes[0,i],
                        levels=[-.5, .5],
                        colors='none',
                        hatches=[None, None, "//", ],
                        add_colorbar=False,
                        extend='both',
                        transform=ccrs.PlateCarree()
                        )

        axes[0, i].set_title(f'RCP26: {file.split("_")[4]}-{file.split("_")[5]}',fontsize=12)

    # Plot data for rcp85
    for i, file in enumerate(sims_rcp85):
        data = xr.open_dataset(file,decode_timedelta=False)
        
        data_variable = data[var]
        
        #data_variable = data['SU35'].dt.days
        im = data_variable.plot(ax=axes[1, i],
                           levels=levels,
                           colors=colors,
                           transform=ccrs.PlateCarree(),
                           extend="both",#"neither",
                           add_colorbar=False,
                           alpha=.8,
                           )
        
        if robustness is True:
            robust_rcp85=file.replace(what,robust) #'time-mean_ensemble-diff-median.nc','ensemble-robustness.nc')
            datar = xr.open_dataset(robust_rcp85)
            datar_variable = datar[var]
            significant = xr.where(~datar_variable.isin([-1, 1, 0]), 1, 0).squeeze()
            significant.plot.contourf(
                    ax=axes[1,i],
                    levels=[-.5, .5],
                    colors='none',
                    hatches=[ None,None,"//", ],
                    add_colorbar=False,
                    extend='both',
                    transform=ccrs.PlateCarree()
            )
        axes[1, i].set_title(f'RCP85: {file.split("_")[4]}-{file.split("_")[5]}',fontsize=12)

    cbar_ax = fig.add_axes([0.15, 0.02, 0.7, 0.03])
    fig.colorbar(im, cax=cbar_ax, orientation="horizontal", label='[ '+unit+' ]')

    name="{}/{}_diff-robust_{}_{}.png".format(plotdir, var, region, user_dpi)

    savefig(plt, "{}".format(name),user_dpi) 
    return

#former plot_6absolut
def plot_absolut(
        sims_rcp26,
        sims_rcp85,
        level_steps, 
        color_steps,    
        plotdir,
        title="",
        var="",
        westafrica=None,
        user_dpi=300,
        rows=2, 
        columns=2,
        ):

    print(sims_rcp26)
    print(sims_rcp85)
    from cartopy import crs as ccrs
    import cartopy.feature as cf
    
    # Some graphical features:
    # set the colors:
    levels=level_steps
    colors=color_steps
    
    font = {
        'family' : 'sans-serif',
        'weight' : 'normal',
    }

    if westafrica is True:
        height=5.2
    else:
        height=7
    if columns == 2:
        width=7
    elif columns == 3:
        width=10
    
    # Create subplots
    fig, axes = plt.subplots(
            ncols=columns, nrows=rows, figsize=(width,height), subplot_kw={'projection': ccrs.PlateCarree()}) 
  
    
    for row in axes:
        for ax in row:
            ax.gridlines(
                draw_labels={"bottom": "x", "left": "y"},
                dms=True,
                x_inline=False,
                y_inline=False,
                linewidth=0.5,
            )
            ax.coastlines(resolution="50m", color="black", linewidth=1)
            ax.add_feature(cf.BORDERS)
            
            #west Afrika
            #lon : -25.87 to 20 by 0.11 degrees
            #lat : -0.75 to 27.3 by 0.11 degrees
            if westafrica is True:
                region='West_Africa'
                ax.set_extent([-25, 20, -0.75, 27.3])
            else:
                region='Africa'
                ax.set_extent([-20, 60, -35, 35])
    
    # Plot data for rcp26
    print('sims_rcp26',sims_rcp26)
    for i, file in enumerate(sims_rcp26):
        print(file)
        data = xr.open_dataset(file,decode_timedelta=False)
        #cha_var(data,var)
        data_variable=get_variable(data,var)
        #data_variable = data[var]
    
        # Select labels // Units frome metadata
        # Set title of plot
        if var !='number_of_people':
            varname=data[var].long_name
            add_unit(data,var)
            unit=data[var].units
        else:
            varname='Number of people'
            unit='Number'
        
        
        s = "{} {}".format(title,varname)
    
        fig.suptitle(s+": ", 
                 fontsize=14, 
                 #fontweight='bold', 
                 x=0.5,
                 position=(0.5, 0.99)
                 )  
                
        im = data_variable.plot(ax=axes[0, i],
                            levels=levels,
                            colors=colors,
                            transform=ccrs.PlateCarree(),
                            extend="both",#"neither",
                            add_colorbar=False,
                            #alpha=.8,
                            )
        # This is not very clever, need to be adjusted according to file_name :-(
        axes[0, i].set_title(f'RCP26: {file.split("_")[5]}-{file.split("_")[6]}',fontsize=12)

    # Plot data for rcp85
    for i, file in enumerate(sims_rcp85):
        data = xr.open_dataset(file,decode_timedelta=False)
        #cha_var(data,var)
        #data_variable = data[var]
        data_variable=get_variable(data,var)
        
        im = data_variable.plot(ax=axes[1, i],
                           levels=levels,
                           colors=colors,
                           transform=ccrs.PlateCarree(),
                           extend="both",#"neither",
                           add_colorbar=False,
                           #alpha=.8,
                           )
        
        axes[1, i].set_title(f'RCP85: {file.split("_")[5]}-{file.split("_")[6]}',fontsize=12)

    cbar_ax = fig.add_axes([0.15, 0.02, 0.7, 0.03])
    fig.colorbar(im, cax=cbar_ax, orientation="horizontal", label='[ '+unit+' ]')

    name="{}/{}_absolut_{}_{}.png".format(plotdir, var, region, user_dpi)

    savefig(plt, "{}".format(name),user_dpi)
    return

def plot_3absolut(
        sim_era5,
        sim_evaluation,
        sim_historical,
        level_steps,
        color_steps,
        plotdir,
        title="",
        var="",
        ):
    from cartopy import crs as ccrs
    import cartopy.feature as cf

    # Some graphical features:
    # set the colors:

    levels = level_steps
    colors = color_steps

    font = {
        'family': 'sans-serif',
        'weight': 'normal',
    }

    # Create subplots
    fig, axes = plt.subplots(
        ncols=3, nrows=1, figsize=(10, 3), subplot_kw={'projection': ccrs.PlateCarree()})
    #all of Africa
        #ncols=3, nrows=1, figsize=(10, 3.5), subplot_kw={'projection': ccrs.PlateCarree()})

    for ax in axes:
        ax.gridlines(
            draw_labels={"bottom": "x", "left": "y"},
            dms=True,
            x_inline=False,
            y_inline=False,
            linewidth=0.5,
        )
        ax.coastlines(resolution="50m", color="black", linewidth=1)
        ax.add_feature(cf.BORDERS)
        #ax.set_extent([-20, 60, -35, 35])
        #west Afrika
        #lon : -25.87 to 20 by 0.11 degrees
        #lat : -0.75 to 27.3 by 0.11 degrees
        ax.set_extent([-25, 20, -0.75, 27.3])

    # Plot era5 data
    data = xr.open_dataset(sim_era5,decode_timedelta=False)
    
    # Select labels // Units frome metadata
    # Set title of plot
    varname=data[var].long_name

    if var =='TG':
        data_variable = data[var]-273.15
        unit='degree Celsius'
    else:
        data_variable = data[var]
        unit=data[var].units
        add_unit(data,var)
      
    s = "{} {}".format(title,varname)
    
    fig.suptitle(s+": ", 
                 fontsize=14, 
                 #fontweight='bold', 
                 x=0.5
                 )  
    
    im = data_variable.plot(ax=axes[0],
                       levels=levels,
                       colors=colors,
                       transform=ccrs.PlateCarree(),
                       extend="both",#"neither",
                       add_colorbar=False,
                       )
    axes[0].set_title(f'ERA5:',fontsize=12)

# Plot evaluation data
    data = xr.open_dataset(sim_evaluation,decode_timedelta=False)
        
    if var =='TG':
        data_variable = data[var]-273.15
    else:
        print('nothing to do')
        
    im = data_variable.plot(ax=axes[1],
                       levels=levels,
                       colors=colors,
                       transform=ccrs.PlateCarree(),
                       extend="both",#"neither",
                       add_colorbar=False,
                       )
    axes[1].set_title(f'Evaluation:',fontsize=12)

# Plot historical data
    data = xr.open_dataset(sim_historical,decode_timedelta=False)
        
    if var =='TG':
        data_variable = data[var]-273.15
    else:
        print('nothing to do')
        
    im = data_variable.plot(ax=axes[2],
                       levels=levels,
                       colors=colors,
                       transform=ccrs.PlateCarree(),
                       extend="both",#"neither",
                       add_colorbar=False,
                       )
    axes[2].set_title(f'historical:',fontsize=12)

    cbar_ax = fig.add_axes([0.15, 0.02, 0.7, 0.05])
    fig.colorbar(im, cax=cbar_ax, orientation="horizontal", label='[ '+unit+' ]')

    name="{}/{}_change.png".format(plotdir, var)

    savefig(plt, "{}".format(name),300) # dpi should be 1200 for a publication
    
    return