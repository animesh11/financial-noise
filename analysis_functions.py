from pandas import Series, DataFrame
import pandas as pdX
from datetime import datetime, timedelta
import numpy as np
import pandas.core.common as com
import pandas.core.algorithms as algos

import pandas.tools.tile

def rolling_timeslice_apply(data, window, func,min_periods=1,direc='F'):

    def f(x):
        '''Function to apply that actually computes the rolling mean'''
        
        time_slice = col[str(x):str(x+pdX.datetools.to_offset(window).delta)]
        if(direc == 'B'):
            time_slice = col[str(x-pdX.datetools.to_offset(window).delta):str(x)][::-1]
        if time_slice.size < min_periods:
            return np.nan
        else:
            return func(time_slice)
    
    data = DataFrame(data.copy())
    dfout = DataFrame()
    if isinstance(window, basestring):
        idx = Series(data.index.to_pydatetime(), index=data.index)
        for colname, col in data.iterkv():
            result = idx.apply(f)
            result.name = colname
            dfout = dfout.join(result, how='outer')
    if dfout.columns.size == 1:
        dfout = dfout.ix[:,0]
    return dfout

def classify_to_dict(seq, key_func):
    result = {}
    for item in seq:
        key = key_func(item)
        if key in result:
            result[key].append(item)
        else:
            result[key] = [item]
    return result

                
def rmg_qcut(x, q, labels=None, retbins=False, precision=3):
    if com.is_integer(q):
        quantiles = np.linspace(0, 1, q + 1)
    else:
        quantiles = q
    bins = algos.quantile(x, quantiles)
    bins = np.unique(bins)
    return pandas.tools.tile._bins_to_cuts(x, bins, labels=labels, retbins=retbins,
        precision=precision, include_lowest=True)



