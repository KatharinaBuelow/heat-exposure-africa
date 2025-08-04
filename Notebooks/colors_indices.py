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


def colorsteps_diff(var):
    """
    Function to define color steps and levels for difference plots
    :param var: variable name
    :return: color_steps_diff, level_steps_diff
    """
    
    if var in ['TR', 'SU35', 'HSx', 'HSn', 'SU40']:
        color_steps_diff = ['#d1e5f0', '#ffffff', '#f7f4f9', '#e7e1ef', '#d4b9da', '#c994c7', '#df65b0', '#e7298a',
                            '#ce1256', '#980043', '#67001f']
    elif var in ['HSf', ]:
        color_steps_diff = ['#92c5de', '#d1e5f0', '#ffffff', '#ffffff', '#f7f4f9', '#e7e1ef', '#d4b9da', '#c994c7',
                            '#df65b0', '#e7298a', '#ce1256', '#980043', '#67001f']
    elif var in ['HWf', ]:
        color_steps_diff = ['#92c5de', '#d1e5f0', '#ffffff', '#ffffff', '#ffffcc', '#ffeda0', '#fed976',
                            '#feb24c', '#fd8d3c', '#fc4e2a', '#e31a1c', '#bd0026', '#800026']
    # Warmspell with tasmax>30
    elif var in ['SU30', 'HWx', 'HWn']:
        color_steps_diff = ['#d1e5f0', '#ffffff', '#ffffcc', '#ffeda0',
                            '#fed976','#feb24c','#fd8d3c','#fc4e2a','#e31a1c','#bd0026','#800026']
    elif var in ['DTR']:
        color_steps_diff = ['#67001f', '#b2182b', '#d6604d', '#f4a582', '#fddbc7', '#f7f7f7', '#d1e5f0', '#92c5de', '#4393c3', '#2166ac', '#053061']
        color_steps_diff = color_steps_diff[::-1]
    # difference plots for WSDI
    elif var in ['WSDI']:
        color_steps_diff = ['#ffffff', '#ffffcc', '#ffeda0', '#fed976', '#feb24c', '#fd8d3c', '#fc4e2a', '#e31a1c', '#bd0026', '#800026', '#7a0177', '#49006a']
    # difference plots of TG:
    elif var in ['TG']:
        color_steps_diff = ['#ffffff', '#ffffcc', '#ffeda0', '#fed976', '#feb24c', '#fd8d3c', '#fc4e2a', '#e31a1c', '#bd0026', '#800026', '#ae017e', '#7a0177', '#49006a']
    else:
        print('no colors defined for ', var)

    if var in ['TR', 'SU30', 'SU35', 'HSn', 'SU40']:
        level_steps_diff = [0, 5, 10, 15, 20, 30, 45, 60, 90, 120]
    elif var == 'HWn':
        level_steps_diff = [0, 10, 20, 30, 60, 90, 120, 150, 180, 220]
    elif var in ['HSx', 'HWx']:
        level_steps_diff = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
    elif var in ['HSf', 'HWf']:
        level_steps_diff = [-3, -1, 0, 1, 3, 5, 7, 9, 11, 13]
    elif var == 'TG':
        level_steps_diff = [-0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
    elif var == 'DTR':
        level_steps_diff = [-2.5, -2, -1.5, -1, -0.5, 0.5, 1, 1.5, 2, 2.5]
    elif var == 'WSDI':
        level_steps_diff = [0, 20, 40, 60, 80, 100, 150, 200, 250, 300, 350]
    else:
        print('no level_steps for ' + var + ' are provided')

    return color_steps_diff, level_steps_diff


def colorsteps_absolute(var):
    """
    Function to define color steps and levels for absolute plots
    :param var: variable name
    :return: color_steps, level_steps
    """
    # Colors and levels for the plots
    # for absolute plots year

    if var in ['TR','SU35','SU30','SU40','HSn']:
        color_steps=['#d9d9d9','#ffffff','#fff7f3','#fde0dd','#fcc5c0','#fa9fb5','#f768a1','#dd3497','#ae017e','#7a0177','#807dba','#6a51a3','#54278f','#3f007d']
    elif var in ['TG','DTR']:
        color_steps=['#d9d9d9','#ffffff','#ffffcc','#ffeda0','#fed976','#feb24c','#fd8d3c','#fc4e2a','#e31a1c','#bd0026','#800026']
    elif var in ['HSx','HSf','HWf','HWn','HWx']:
        color_steps=['#d9d9d9','#ffffff','#f7f4f9','#e7e1ef','#d4b9da','#c994c7','#df65b0','#e7298a','#ce1256','#980043','#67001f']
    else:
        print('no color steps defined')

    if var=='TR':
        level_steps=[0,30,60,90,120,150,180,210,240,270,300,330,360]
    elif var=='TG':
        level_steps=[0,10,15,18,21,24,27,30,33]
    elif var=='DTR':
        level_steps=[0,6,8,10,12,14,16,17,18]
    elif var in ['SU30','SU35','HSn']:
        level_steps=[0,30,60,90,120,150,180,210,240,270,300,330,360]  
    elif var in ['SU40']:
        level_steps=[0,10,20,30,40,50,60,70, 80,90,100,120,140]
    elif var in ['HSx','HWx']:
        level_steps=[0,30,60,90,120,150,180,210,240]
    else:
        print('no level_steps for '+ var+' are provided')
    return color_steps, level_steps

