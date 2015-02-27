from __future__ import division
print "Doing Initial Configuration.....Please wait....it's a lot of work!"
print "************************"

import sys
import pandas as pd
import os
import re
import numpy as np
import scipy 
from scipy.optimize import minimize
import datetime
import calendar
#Parallel processing
from multiprocessing import Process

import collections
import yaml
import numpy as np

script_year = 2014
bucket_size = 7

def calib_func(x,data,buckets,option,minfactor,maxfactor):
    if(option == 'no'):
        minfactor = np.percentile(data['factor1'].values,2)
        maxfactor = np.percentile(data['factor1'].values,98)
        
    #Limit movement outside model bounds 
    if(option == 'yes'):
        data['factor1'][data['factor1']>=maxfactor] = maxfactor
        data['factor1'][data['factor1']<=minfactor] = minfactor

    #The second layer of this simplfied neural network controls the trend load
    factorload2 = 1.0/(1.0+np.exp(-x[3]*data['range']/data['duration']))
    #Scale this layer without allowing fixed movement
    factorload = x[2]*factorload2 - x[2]/2.0

    #Layer 1 - Main classification factor of neural network
    z = 1.0/(1.0+np.exp(-factorload * x[1] * data['factor1']))
    
    #Sigmoid function is used for classification
    adjustment_series = pd.Series(z)
    #Scale the model
    adjustment_series = x[0]*adjustment_series - x[0]/2
    newprice = data['bs_probability'] + adjustment_series.values

    data['newprice']=newprice
    data['newpnl']=0.0
    data['newpnl'] = data['wins']-data['newprice']
    if(option=='yes'):
        data['factorload']=x[2]*factorload2 - x[2]/2.0
        data['factorload2']=factorload2
        return 1.0
    d1=np.repeat(0.0,7)
    i=0
    ranges = pd.groupby(data,pd.qcut(data['range'],7))
    for mname,m_data in ranges:
        d1[i]=np.mean(pd.groupby(m_data,by=pd.qcut(m_data['factor1'],7)).mean()['newpnl']**2)
        i=i+1
    return np.mean(d1)**0.5

def start_parallel_calibration(underlying,f):
    data = pd.read_csv(underlying+"_model.csv")
    data = data.sort(['date_part'])

    data['bs_probability']=0.499
    data['factor1']=data['trend']/(data['duration']*data['vol']**0.5)
    data =data.set_index([data['date_part'],data['duration']])
    data = data.drop_duplicates()
    data = data.dropna()
    data_insample = data[data['datetimes']<'2014-05-30']
    data_outsample = data[data['datetimes']>'2014-05-30']

    min_exfactor = np.percentile(data_insample['factor1'],2)
    max_exfactor = np.percentile(data_insample['factor1'],98)
    x1 = [0.14166683 ,-0.60474994 , 0.01122884 ,-0.16496619]
    x0 = x1
    p1=scipy.optimize.minimize(calib_func,x0,args=(data,bucket_size,'no',0,0,),method='L-BFGS-B',options={'disp':True})
    calib_func(p1.x,data_outsample,bucket_size,'yes',min_exfactor,max_exfactor)
    data_outsample.to_csv(underlying+str("_auto.csv"))
    
processes = []
#For multiple underlyings map multiple underlyings
p = Process(target=start_parallel_calibration,args=('AS51',0,))
p.start()
processes.append(p)

for p in processes:
    p.join()




