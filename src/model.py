#This is the module for radiative balance related functions
import matplotlib.pyplot as plt 
import pandas as pd
import numpy as np
import math 


#co2 data 
co2_ice_df = pd.read_excel('/home/lyubo/Desktop/climate forcing model/data/law2006.xls', sheet_name= 'CO2 by age')
co2_ice_years = co2_ice_df['CO2 gas age years AD']
co2_ice_ppm = co2_ice_df['CO2 (ppm)']

co2_ml_df = pd.read_csv('/home/lyubo/Desktop/climate forcing model/data/co2_mm_gl.csv', comment='#', skiprows=38)
co2_ml = co2_ml_df['average']

#ch4 data
ch4_ice_df = pd.read_excel('/home/lyubo/Desktop/climate forcing model/data/law2006.xls', sheet_name= 'CH4 by age')
ch4_ice_years = ch4_ice_df['CH4 gas age years AD']
ch4_ice_ppb = ch4_ice_df['CH4 (ppb)']

ch4_g_df = pd.read_csv('/home/lyubo/Desktop/climate forcing model/data/ch4_mm_gl.csv', comment='#',skiprows=45)

# n2o data
n2o_ice_df = pd.read_excel('/home/lyubo/Desktop/climate forcing model/data/law2006.xls', sheet_name= 'N2O by age')
n2o_ice_years = n2o_ice_df['N2O gas age years AD']
n2o_ice_ppb = n2o_ice_df['N2O (ppb)']

n2o_g_df = pd.read_csv('/home/lyubo/Desktop/climate forcing model/data/n2o_mm_gl.csv', comment='#',skiprows=45)


plt.plot(co2_ice_years,co2_ice_ppm)
plt.plot(ch4_ice_years,ch4_ice_ppb)
plt.plot(n2o_ice_years,n2o_ice_ppb)
#plt.show()

#initialize constants(to be user controled later)
l = 0.8 #climate sensitivity
C0 = 278.0 #initial CO2 amount preindustrialization(1750) in ppm
N0 = 0.0
M0 = 0.0

###################################################
#climate forcing and temperature response functions
###################################################

def mean_gas(X, X0) -> float:
    return 0.5*(X+X0)


def rf_co2_basic(C: float,C0: float) -> float:
    """
    Calculate radiative forcing for CO2
    
    This function calculates radiative forcing(W/m2) independent of other GHG concentrations
    """
    return 5.35*math.log(C/C0)

def rf_co2(C, C0,N,N0) -> float: #<-- change dependence on C0 and N0 somehow
    a1 = -2.4e-7 # (W/m2-ppm2)
    b1 = 7.2e-4 # (W/m2-ppm)
    c1 = -2.1e-4 # (W/m2-ppb)
    constant = a1*(C-C0)**2 + b1*abs(C-C0) + c1*mean_gas(N,N0) + 5.36
    delF = constant*math.log(C/C0)
    return delF

def rf_n2o(C,N,M,C0,N0,M0) -> float:
    a2 = -8.0e06 # (W/m2-ppb)
    b2 = 4.2e-6 # (W/m2-ppb)
    c2 = -4.9e-6 # (W/m2-ppb)
    constant = a2*mean_gas(C,C0) + b2*mean_gas(N,N0) + c2*mean_gas(M,M0) +0.117
    delF = constant*(math.sqrt(N)-math.sqrt(N0))
    return delF

def rf_ch4(M,N,M0,N0) -> float:
    a3 = -1.3e-6 # (W/m2-ppb)
    b3 = -8.2e-6 # (W/m2-ppb)
    constant = a3*mean_gas(M,M0) + b3*mean_gas(N,N0) + 0.043
    delF = constant*(math.sqrt(M)-math.sqrt(M0))
    return delF

def rf_total(C,N,M):
    return C + N + M

def temp_anomaly(F) -> float:
    return l * F


delT = []
for i in co2_ml:
    new_delT = temp_anomaly(rf_co2_basic(i,C0))
    delT.append(new_delT)
delT = np.array(delT)
x = np.arange(len(delT))
plt.plot(x,delT)

#plt.show()