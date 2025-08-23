#This is the module for radiative balance related functions

import matplotlib.pyplot as plt 
import pandas as pd
import numpy as np
import math

co2_mm_df = pd.read_csv('/home/lyubo/Desktop/climate forcing model/data/co2_mm_gl.csv', comment='#', skiprows=38)
co2_mm = co2_mm_df['average']

#co2_mm.plot()


#initialize constants
l = 0.8 #climate sensitivity
C0 = 278 #initial CO2 amount preindustrialization

#climate forcing and temperature response functions

def calc_delF(C,C0):
    return math.log(5.35*(C+C0)/C0)

def calc_delT(F):
    return l * F

delT = []
for i in co2_mm:
    new_delT = calc_delT(calc_delF(i,C0))
    delT.append(new_delT)
delT = np.array(delT)
x = np.arange(len(delT))
plt.plot(x,delT)

plt.show()