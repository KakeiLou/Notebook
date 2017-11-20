
# coding: utf-8

# In[1]:

#本版本已修改观察日为开始时期按月增加，如果那天不是交易日，则移动至下一个交易日
#2.0 现在版本支持任意合约月份输入了！修复了提前敲出时收益率亏损的问题
#增加了敲出价格的比例设置
import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta
get_ipython().magic('matplotlib inline')


# In[2]:

def get_obs_ndays(dt,m):
    dt = pd.to_datetime(dt)
    l =[]
    for i in range(m):
        day = dt + relativedelta(months= i+1)
        l.append(day)
    return l


# In[3]:

def split_ndf(df,dt,months):
    dt = pd.to_datetime(dt)
    l = get_obs_ndays(dt,months+1)
    list=[]
    df1 = df[dt:l[0]]
    list.append(df1)    
    for i in range(months):
        dfi = df[l[i]:l[i+1]]
        list.append(dfi)
    return list


# In[4]:

def judge_tradeday(dl,dlis,months):
    for i in range(months):
        if dl[i] in dlis[i].index:
            #print ('No change')
            continue
        else:
            dl[i] = dlis[i+1][0:1].index
            pydate_array = dl[i].to_pydatetime()
            date_only_array = np.vectorize(lambda s: s.strftime('%Y-%m-%d'))(pydate_array )
            date_only_series = pd.Series(date_only_array)
            dl[i] = date_only_series[0]
            dl[i] = pd.to_datetime(dl[i])
            dl[i] = dl[i] + relativedelta(months=0)
            #print (dl[i])
    return dl


# In[13]:

def month_pro(df, jt, open_price, lowerbond, rate):
    knock_out = 0
    profit = 0
    loss= 0
    m = df[df.index == jt]
    a = m.close.max()
    b = open_price.close.max()
    c = lowerbond.close.max()
    if a > b:
        #print ('knock-out, knock-out!')
        profit = rate
        knock_out = 1
    elif a >= c:
        profit = rate
        
    else:
        profit = 0
    return [knock_out, profit]   


# In[14]:

def knock_in(df, dt, mths, lowerbond):
    knock_in = 0
    dt = pd.to_datetime(dt)
    y = dt + relativedelta(months= mths )
    df1 = df[dt:y]
    #df1.plot()
    if np.isnan(df1[df1 < lowerbond.close.min()].close.min())== 1:
        #print ('did not knock-in!' )
        knock_in =1
        return knock_in
    else: 
        #print ('knock-in, knock-in!')
        return knock_in


# In[15]:

def final_rtn(df,dt,open_price, mths, m,cum_pro):
    dt = pd.to_datetime(dt)
    y = dt + relativedelta(months= mths )
    df1 = df[dt:y]
    #print (df1[-1:].close)
    if ((df1[-1:].close.min() < open_price.close.min()) and (m == 0) )== True:
        final_rtn = cum_pro + ((df1[-1:].close.min() - open_price.close.min())/open_price.close.min())
        #print('hi')
    else:
        final_rtn = cum_pro
    return final_rtn


# In[39]:

def phoenix_rtn(df, dt, months, rtn_rate, low_rate=0.7, high_rate =1.0):
    obdays = get_obs_ndays(dt,months)
    list = split_ndf(df, dt, months)
    jt = judge_tradeday(obdays,list,months)
    open_price = list[0][0:1]*high_rate
    lowerbond = open_price*low_rate
    cum_pro = 0
    real_months = months
    for i in range(months):
        result = month_pro(df, jt[i], open_price, lowerbond, rtn_rate)
        cum_pro = cum_pro + result[1]
        if result[0] == 1:
            real_months = i+1
            break
    m = knock_in(df, dt, months,lowerbond)
    total_rtn = final_rtn(df, dt, open_price, real_months, m, cum_pro)
    return total_rtn


# In[294]:

#df = pd.read_hdf('C:/Users/Administrator/Desktop/Work/Projects/Autocall/new000905.h5')
#df.index = pd.to_datetime(df.index)
#df


# In[295]:

#phoenix_rtn(df, '2016-11-14', 4, 0.04, 0.7)


# In[44]:

df1 = pd.read_excel('C:/Users/Administrator/Desktop/Work/Projects/Autocall/fake_test_data.xlsx')
df1.index = df1.day
df1.drop('day',axis=1,inplace=True)
df1.columns = ['close']
phoenix_rtn(df1, '2017-1-5', 9, 0.025,0.7)


# In[297]:

#phoenix_rtn(df1, '2017-1-5', 6,0.025,0.7)


# In[ ]:



