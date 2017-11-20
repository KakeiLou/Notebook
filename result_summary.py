
# coding: utf-8

# In[6]:

import pandas as pd
import numpy as np
from datetime import datetime 
import os
import transcation as tran
import tushare as ts
get_ipython().magic('matplotlib inline')
import pyfolio as pf
import pandas as pd
import matplotlib as mpl
mpl.rcParams["figure.facecolor"] = "white"
mpl.rcParams["axes.facecolor"] = "white"
mpl.rcParams["savefig.facecolor"] = "white"


# 读取交易日历

# In[12]:

dfday = pd.read_csv('tradeDate.csv')
dfday.columns = ['zzz','calendarDate']
dfday.drop('zzz',axis=1,inplace=True)
dates = list(dfday.calendarDate)


# 晚上交易的算下一个交易日

# In[13]:

def business_date(t):
    if t.hour > 15: # afternoon
        return dates[dates.index(t.strftime('%Y-%m-%d')) + 1]
    else:
        return t.strftime('%Y-%m-%d')


# 返回所有交易记录

# In[15]:

def find_transaction(path):
    dfs = []
    for f in os.listdir(path):
        if f.find('orders.csv') == -1:
            continue
        df = pd.read_csv(os.path.join(path, f), index_col=0, parse_dates=True, 
                         header=None, names=['order_id', 'open_close', 'direction', 'status', 'price', 'lots'])
        df['instrument'] = f[:f.find('_')]
        dfs.append(df)
    df = pd.concat(dfs)
    df = df[df.status == 1]
    df.sort_index(inplace=True)
    df.index.name = 'datetime'
    df.reset_index(inplace=True)
    df['real_trade_date'] = df.datetime.apply(business_date)
    df.set_index('datetime', inplace=True)
    df.open_close = df.open_close.apply(lambda x : 0 if x == 'O' else 1)
    df.direction = df.direction.apply(lambda x : 0 if x == 'B' else 1)
    return df
    


# 读取合约的每天收益净值

# In[28]:

def find_instrument_equitys(path,instrument):
    df = pd.read_csv(os.path.join(path, '%s_equitys.csv' % instrument), header=None, names=['timestamp', 'equitys', 'pnl', 'fee'])
    df['datetime'] = (df.timestamp/1000.0).apply(datetime.utcfromtimestamp)
    return df


# 计算策略所有合约收益率

# In[4]:

def calc_instrument_rets(path):
    instruments = []
    for i in os.listdir(path):
        if i.find('equitys.csv')== -1:
            continue
        instruments.append(i[:i.find('_')])
    dfs = []
    for instrument in  instruments:
        df = pd.read_csv(os.path.join(path, '%s_equitys.csv' % instrument), header=None, names=['timestamp', 'equitys', 'pnl', 'fee'])
        df['instrument']  = instrument
        dfs.append(df)
    df = pd.concat(dfs)
    equitys = df.groupby('instrument')['equitys'].last()
    return equitys / 500000.0 - 1


# In[5]:

def rtn_compare(benchmark,path):
    df = pd.DataFrame([calc_instrument_rets(path),calc_instrument_rets(benchmark)], index=['backtest', 'benchmark']).T
    df['change'] = df.backtest - df.benchmark
    df = df.sort_values('change')
    return df


# In[11]:

#benchmark = 'C:/Users/Administrator/Desktop/Work/data/CTA_algo/backtesting/result0_0/'
#path = 'C:/Users/Administrator/Desktop/Work/data/CTA_algo/backtesting/result0_0/'
#instrument = 'fg709'


# 计算每日收益

# In[26]:

def calc_daily_rets(path):
    instruments = []
    for i in os.listdir(path):
        if i.find('equitys.csv')== -1:
            continue
        instruments.append(i[:i.find('_')])
    dfs = []
    for instrument in  instruments:
        df = pd.read_csv(os.path.join(path, '%s_equitys.csv' % instrument), header=None, names=['timestamp', 'equitys', 'pnl', 'fee'])
        df['instrument']  = instrument
        df['pnl_change'] = df.equitys - df.equitys.shift(1)
        df.pnl_change = df.pnl_change.fillna(0)
        dfs.append(df)
    df = pd.concat(dfs)
    df['datetime'] = (df.timestamp/1000.0).apply(datetime.utcfromtimestamp)  
    pnl_changes = df.groupby(df.datetime.dt.date)['pnl_change'].sum()
    cumsum_pnl_changes = pnl_changes.cumsum()
    equitys = cumsum_pnl_changes + 500000
    return (equitys/equitys.shift(+1) - 1)


# 回测结果绘表

# In[19]:

def result_pf(path,benchmark):   
    rets = calc_daily_rets(path)
    ben_rets = calc_daily_rets(benchmark)
    pf.create_simple_tear_sheet(rets, benchmark_rets=ben_rets, live_start_date=None)


# 计算一个品种每日收益

# In[82]:

def calc_instrument_daily_ret(df):
    df['date'] = (df.timestamp/1000.0).apply(datetime.utcfromtimestamp)
    df.set_index('date', inplace=True)
    return (df.equitys.shift(-1)/df.equitys - 1)


# 返回一个品种的回测结果

# In[1]:

def instrument_result_pf(instrument,path,benchmark,start_date):
    df = pd.read_csv(os.path.join(path, '%s_equitys.csv' % instrument), header=None, names=['timestamp', 'equitys', 'pnl', 'fee'])
    benchmark_df = pd.read_csv(os.path.join(benchmark, '%s_equitys.csv' % instrument), header=None, names=['timestamp', 'equitys', 'pnl', 'fee'])
    rets = calc_instrument_daily_ret(df)
    benchmark_rets = calc_instrument_daily_ret(benchmark_df)
    pf.create_simple_tear_sheet(rets, benchmark_rets=benchmark_rets, live_start_date=start_date)


# 返回所有回测结果里各品种的最大收益和基准收益做比较

# In[9]:

def max_instrument_rtn(df,benchmark):
    df=df.T
    sr1 = df.max()
    sss =  calc_instrument_rets(benchmark)
    dfmax = pd.DataFrame([sr1,sss])
    dfmax = dfmax.T
    dfmax.columns = ['maxvalue','benchmark']
    dfmax['diff'] = dfmax.maxvalue - dfmax.benchmark
    return dfmax


# In[ ]:




# In[ ]:




# In[ ]:



