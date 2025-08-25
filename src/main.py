#This is the place to execute the main code for stage 1
#This code will: 
# initialize constants(climate sensitivity, initial gas concentrations)
# read GHG data(use functions, os relative path)
# compile into numpy arrays, 
# run model functions, 
# create necessary output arrays for visualization
# run visualization code

import matplotlib.pyplot as plt 
import pandas as pd
import numpy as np
import math 
import os
import model


DATA_PATH = os.path.abspath('data/')
t0 = 1750

def read_ice_data(G: str):
    '''
    Read law2006.xls data  
    
    This function returns a NumPy array of time and concentration
    data for a specified gas(G)
    '''
    array = [[],[]]
    ice_df = pd.read_excel(f'{DATA_PATH}/law2006.xls', sheet_name= f"{G.upper()} by age")
    ice_years = ice_df[f'{G.upper()} gas age years AD']
    array[0].extend(ice_years)
    if f'{G.upper()} (ppm)' in ice_df:
        ice_ppm = ice_df[f'{G.upper()} (ppm)']
        array[1].extend(ice_ppm)
    elif f'{G.upper()} (ppb)' in ice_df:
        ice_ppb = ice_df[f'{G.upper()} (ppb)']
        array[1].extend(ice_ppb)
    return np.array(array)

def read_mauna_loa():
    '''
    Read CO2 Mauna Loa dataset

    This function reads the ML dataset and returns a NumPy array
    of time and concentration(ppm) for CO2
    '''
    array = [[],[]]
    co2_ml_df = pd.read_csv(f'{DATA_PATH}/co2_mm_gl.csv', comment='#', skiprows=38)
    co2_ml_ppm = co2_ml_df['average']
    co2_ml_years = co2_ml_df['decimal']
    array[0].extend(co2_ml_years)  
    array[1].extend(co2_ml_ppm)
    return np.array(array)

def read_global_data(G: str):
    '''
    Read global atmospheric concentration data

    This function reads global monthly mean datasets for either CH4 or N2O
    and returns a NumPy array of time and concentration(ppb)
    '''
    array = [[],[]]
    g_df = pd.read_csv(f'{DATA_PATH}/{G.lower()}_mm_gl.csv', comment='#',skiprows=45)
    g_years = g_df['decimal']
    g_ppb = g_df['average']
    array[0].extend(g_years)
    array[1].extend(g_ppb)
    return np.array(array)

def combine_data(ice,present):
    '''
    Combine ice and present data

    This function combines the past(ice core) and present(ML or global) datasets for CO2, CH4, or N2O 
    and cuts off the data at a specified start time(t0)
    '''
    array = [[],[]]
    for i in reversed(range(len(ice[0]))):
        if ice[0][i] < t0:
            pass
        elif ice[0][i] >= min(present[0]):
            pass
        else:
            array[0].append(ice[0][i])
            array[1].append(ice[1][i])
    for i in range(len(present[0])):
        array[0].append(present[0][i])
        array[1].append(present[1][i])            
    return np.array(array)


def main() -> None:
    #Read datasets
    co2_ice = read_ice_data('co2')
    ch4_ice = read_ice_data('ch4')
    n2o_ice = read_ice_data('n2o')
    co2_ml = read_mauna_loa()
    ch4_g = read_global_data('ch4')
    n2o_g = read_global_data('n2o')

    #Combine datasets
    co2 = combine_data(co2_ice,co2_ml)
    ch4 = combine_data(ch4_ice,ch4_g)
    n2o = combine_data(n2o_ice,n2o_g)


if __name__=='__main__':
    main()