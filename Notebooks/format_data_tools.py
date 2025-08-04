#!/usr/bin/env python3

import os
import pandas as pd

import numpy as np
import glob
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import xarray as xr
import cftime


def directory_available(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    return


def decode_time_pop(ds):
    #time axis needs to be defined for the population data
    time_vals = ds.time.values
    
    decoded_times = cftime.num2date(
        time_vals*365.25,
        units="days since 1661-1-1 00:00:00",
        calendar="proleptic_gregorian"
    )
    # Neue Zeitkoordinate setzen
    return ds.assign_coords(time=("time", decoded_times))


def save_file_to_netcdf(df, outpath, filename):
    # save the dataframe to a netcdf file
    return df.to_netcdf(outpath + filename, format='NETCDF4')
