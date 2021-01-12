#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 20:01:59 2021

@author: marcos
"""
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import numpy as np
import pandas
import statsmodels.api as sm # to build a LOWESS model
import os

lowess = sm.nonparametric.lowess
root=tk.Tk()
root.withdraw()
file_path=filedialog.askopenfilename()
esn=os.path.basename(file_path)[0:6]

df = pandas.read_table(file_path, delim_whitespace=True, names=('TSN', 'OIL', 'HOURS'),
                   dtype={'TSN': np.float64, 'Oil': np.float64, 'Hours': np.float64})
array = df.values
dataset = array[:,0:3]

contador=0

total_time=0
total_rep=0
hours=[]
rep=[]
tsn=[]
consump=[]
maxc=[]
calcs=[]
outF = open("OutFile - %s.txt"% (esn), "w")
outF.write(str(['TSN','OIL','HOURS','CONSUMP','MAX']).strip('[]'))
while (contador<len(dataset)):
    total_time=total_time+dataset[contador,2];
    total_rep=total_rep+dataset[contador,1];
    if (total_time>39) and (total_time<55):
        consump.append(total_rep/total_time)
        hours.append(total_time)
        rep.append(total_rep)
        tsn.append(dataset[contador,0])
        maxc.append(0.270)
        calcs=[dataset[contador,0],total_rep,total_time,total_rep/total_time,0.270]
        outF.write("\n")
        outF.write(str(calcs).strip('[]'))
        total_time=0
        total_rep=0
    contador=contador+1
outF.close()
y_hat1 = lowess(consump,tsn,frac=1/5)

plt.rcParams["figure.dpi"] = 300
plt.Figure(figsize=(4,3))
plt.grid(which='both', axis='both')
plt.plot(tsn, consump,'-s', color='blue', label='Consumo', linewidth=0.5)
plt.plot(tsn, maxc,'--', color='black', label='Max',linewidth=0.5)
plt.plot(tsn, y_hat1[:,1],'--', color='red', label='LOWESS', linewidth=0.5)
plt.title("ESN: PCE-%s" % (esn))
plt.xlabel('TSN (Hours)')
plt.ylabel('Consumption (Rep/Hours)')
plt.savefig("PCE-%s.png" % (esn))