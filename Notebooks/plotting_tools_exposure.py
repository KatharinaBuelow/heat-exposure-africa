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
    return


def plot_2diff_pop(
        pop_diff_ssp1,
        pop_diff_ssp3,
        plotdir,
        title="",
        var="",
        westafrica=None,
        user_dpi=300,
        ):

    from cartopy import crs as ccrs
    import cartopy.feature as cf
    
    # Some graphical features:
    # set the colors:
    levels=[0,10,20,30,40,50,60,70,80,90,100,110]
    colors=['#a50026','#d73027','#f46d43',
             '#fdae61','#fee08b',
             '#ffffbf','#d9ef8b','#a6d96a',
             '#66bd63','#1a9850','#006837',
             '#ffffff','#d9d9d9']
    
    # Reverse the color order for better visual effect
    colors = colors[::-1]

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

        if westafrica is True:
            region='West_Africa'
            ax.set_extent([-25, 20, -0.75, 27.3])
            # Space between rows:
            fig.subplots_adjust(hspace=0.03)
        else:
            region='Africa'
            ax.set_extent([-20, 60, -35, 35])

    # Plot data for ssp1
    for i, file in enumerate(pop_diff_ssp1):
        print('file: ',file)
        data = xr.open_dataset(file,decode_timedelta=False)
        data_variable = data[var]/1000
        
        varname='Number of People'
        unit='Number*10³'
        
        s = "{} [{}]".format(title,varname)
    
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
        ax1.set_title(f'ssp1: {file.split("_")[2]}-{file.split("_")[3]}',fontsize=12)

    # Plot data for ssp3
    for i, file in enumerate(pop_diff_ssp3):

        data = xr.open_dataset(file,decode_timedelta=False)
        data_variable = data[var]/1000
        im = data_variable.plot(ax=ax2,
                           levels=levels,
                           colors=colors,
                           transform=ccrs.PlateCarree(),
                           extend="both",#"neither",
                           add_colorbar=False,
                           alpha=.8,
                           )
        
        ax2.set_title(f'ssp3: {file.split("_")[2]}-{file.split("_")[3]}',fontsize=12)

    cbar_ax = fig.add_axes([0.15, 0.1, 0.7, 0.05])
    fig.colorbar(im, cax=cbar_ax, orientation="horizontal", label='[ '+unit+' ]')

    name="{}/{}_diff_{}_{}.png".format(plotdir, var, region, user_dpi)

    savefig(plt, "{}".format(name),user_dpi) 
    return


def plot_absolute_pop(
        pop_ssp1,
        pop_ssp3,   
        plotdir,
        title="",
        var="",
        westafrica=None,
        user_dpi=300,
        rows=2, 
        columns=2,
        ):

    print(pop_ssp1)
    print(pop_ssp3)

    from cartopy import crs as ccrs
    import cartopy.feature as cf
    
    # Some graphical features:
    # set the colors, special case for population:
    levels=[0,5,10,20,30,60,90,120,150,180,210,240,270]
    colors=['#d9d9d9','#ffffff','#f5f5f5','#c7eae5',
            '#80cdc1','#66c2a4','#35978f','#01665e','#003c30',
            '#f6e8c3',
            '#dfc27d','#bf812d',"#a35414","#854e0c",'#543005',]
    
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
            
            if westafrica is True:
                region='West_Africa'
                ax.set_extent([-25, 20, -0.75, 27.3])
            else:
                region='Africa'
                ax.set_extent([-20, 60, -35, 35])
    
    # Plot data for ssp1

    for i, file in enumerate(pop_ssp1):
        print(file)
        data = xr.open_dataset(file,decode_timedelta=False)
        data_variable=data[var]/1000    
        # Select labels // Units frome metadata
        # Set title of plot
        if var =='number_of_people':
            varname='Number of People'
            unit='Number * 10³'

        s = "{} {}".format(varname, title)
    
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
        axes[0, i].set_title(f'ssp1: {file.split("_")[1]}-{file.split("_")[2]}',fontsize=12)

    # Plot data for ssp3
    for i, file in enumerate(pop_ssp3):
        data = xr.open_dataset(file,decode_timedelta=False)
        data_variable=data[var]/1000
        if var =='number_of_people':
            varname='Number of People'
            unit='Number *10³'
        im = data_variable.plot(ax=axes[1, i],
                           levels=levels,
                           colors=colors,
                           transform=ccrs.PlateCarree(),
                           extend="both",#"neither",
                           add_colorbar=False,
                           #alpha=.8,
                           )
        
        axes[1, i].set_title(f'SSP3: {file.split("_")[1]}-{file.split("_")[2]}',fontsize=12)

    cbar_ax = fig.add_axes([0.15, 0.02, 0.7, 0.03])
    fig.colorbar(im, cax=cbar_ax, orientation="horizontal", label='[ '+unit+' ]')

    name="{}/{}_absolut_{}_{}.png".format(plotdir, var, region, user_dpi)

    savefig(plt, "{}".format(name),user_dpi)
    return

def plot_2_diff_exposure(
        exposure_ssp1,
        exposure_ssp3,
        robust_rcp26,
        robust_rcp85,
        plotdir,
        title="",
        var="",
        varr="",
        robustness=False,
        westafrica=None,
        user_dpi=300,
        ):

    from cartopy import crs as ccrs
    import cartopy.feature as cf
    
    #import matplotlib.pyplot as plt

    from matplotlib.colors import ListedColormap

    # Some graphical features:
    # set the colors:
    levels=[0,1,2,3,4,5,6,7,8,9,10]
    colors=['#d9d9d9',"#fdfde8",'#ffffcc','#ffeda0','#fed976',
            '#feb24c','#fd8d3c','#fc4e2a',
            '#e31a1c','#bd0026','#800026',"#4B0117"]
    
    
    custom_cmap = ListedColormap(colors)
    custom_cmap.set_bad(color='white')

    hatchcolor='grey'
    plt.rcParams.update({'hatch.color': hatchcolor})
    plt.rcParams["font.family"] = "sans-serif"    
    
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

        if westafrica is True:
            region='West_Africa'
            ax.set_extent([-25, 20, -0.75, 27.3])
            # Space between rows:
            fig.subplots_adjust(hspace=0.03)
        else:
            region='Africa'
            ax.set_extent([-20, 60, -35, 35])

    # Plot data for ssp1-rcp26
    
    data = xr.open_dataset(exposure_ssp1,decode_timedelta=False)
    data_variable = data[var]/1000000
    mask_data= data_variable.where(data[var] != 0)
    varname='Exposure'
    unit='Person-Events *10⁶'

    s = "{} {}".format(title,varname)
    
    fig.suptitle(s+": ", 
                 #fontweight='bold', 
                 x=0.5,
                 fontsize=14,
                 position=(0.5, 0.99),
                 )  

    im = mask_data.plot(ax=ax1,
                            levels=levels,
                            cmap=custom_cmap,
                            transform=ccrs.PlateCarree(),
                            extend="both",#"neither",
                            add_colorbar=False,
                            alpha=.8,
                            )
    if robustness is True:
            datar = xr.open_dataset(robust_rcp26)
            datar_variable = datar[varr]  
            significant = xr.where(~datar_variable.isin([-1, 1, 0]), 1, 0).squeeze()
            significant.plot.contourf(
                        ax=ax1,
                        levels=[-.5, .5],
                        colors='none',
                        hatches=[None, None, "//", ],
                        add_colorbar=False,
                        extend='both',
                        transform=ccrs.PlateCarree()
                        )

    ax1.set_title(f'SSP1/RCP26: {robust_rcp26.split("_")[5]}-{robust_rcp26.split("_")[6]}',fontsize=12)

    # Plot data for rcp85
    data = xr.open_dataset(exposure_ssp3,decode_timedelta=False)
    data_variable = data[var]/1000000
    mask_data= data_variable.where(data[var] != 0)

    im = mask_data.plot(ax=ax2,
                       levels=levels,
                       cmap=custom_cmap,
                       transform=ccrs.PlateCarree(),
                       extend="both",#"neither",
                       add_colorbar=False,
                           alpha=.8,
                           )
        
    if robustness is True:
        datar = xr.open_dataset(robust_rcp85)
        datar_variable = datar[varr]
        significant = xr.where(~datar_variable.isin([-1, 1, 0]), 1, 0).squeeze()
        significant.plot.contourf(
                    ax=ax2,
                    levels=[-.5, .5],
                    colors='none',
                    hatches=[ None,None,"//", ],
                    add_colorbar=False,
                    extend='both',
                    transform=ccrs.PlateCarree()
            )
        ax2.set_title(f'SSP3/RCP85: {robust_rcp85.split("_")[5]}-{robust_rcp85.split("_")[6]}',fontsize=12)

    cbar_ax = fig.add_axes([0.15, 0.1, 0.7, 0.05])
    fig.colorbar(im, cax=cbar_ax, orientation="horizontal", label='[ '+unit+' ]')

    name="{}/{}_diff-robust_{}_{}.png".format(plotdir, var, region, user_dpi)

    savefig(plt, "{}".format(name),user_dpi) 
    return
