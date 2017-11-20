import numpy as np
import pandas as pd
from math import log,sqrt,exp
from scipy import stats


def Black_call_value(F0, K, t, T, r, sigma):
    F0 = float(F0)
    d1 = (log(F0/K) + (sigma**2)*(T-t)*0.5)/(sigma*sqrt(T-t))
    d2 = (log(F0/K) - (sigma**2)*(T-t)*0.5)/(sigma*sqrt(T-t))
    Black_value = exp(- r * (T-t))*(F0*stats.norm.cdf(d1,0.0,1.0) - K *stats.norm.cdf(d2,0.0,1.0))
    return Black_value

def Black_call_Delta(F0, K,t ,T ,r , sigma):
    F0 = float(F0)
    d1 = (log(F0/K)+(sigma**2)*(T-t)*0.5)/(sigma*sqrt(T-t))
    d2 = (log(F0 / K) - (sigma ** 2) * (T - t) * 0.5) / (sigma * sqrt(T - t))
    delta = exp(-r*(T-t))*stats.norm.cdf(d1,0.0,1.0)
    return delta

def Black_call_Vega(F0, K, t, T,r, sigma):
    F0 = float(F0)
    d1 = (log(F0/K)+(sigma**2)*(T-t)*0.5)/(sigma*sqrt(T-t))
    d2 = (log(F0 / K) - (sigma ** 2) * (T - t) * 0.5) / (sigma * sqrt(T - t))
    vega = F0*exp(-r*(T-t))*stats.norm.pdf(d1,0.0,1.0)*sqrt(T-t)
    vega = vega/100
    #波动率每增加1%，期权价格的变化量
    return vega

def Black_call_Theta(F0, K, t, T,r, sigma):
    F0 = float(F0)
    d1 = (log(F0/K)+(sigma**2)*(T-t)*0.5)/(sigma*sqrt(T-t))
    d2 = (log(F0 / K) - (sigma ** 2) * (T - t) * 0.5) / (sigma * sqrt(T - t))
    theta = (-(F0*exp(-r*(T-t))*stats.norm.pdf(d1,0.0,1.0)*sigma)/(2*sqrt(T-t))) + (r*F0*exp(-r*(T-t))*stats.norm.cdf(d1,0.0,1.0)) -(r*K*exp(-r*(T-t))*stats.norm.cdf(d2,0.0,1.0))
    theta = theta/365
    #剩余天数mei增加一天，期权价格的变化量
    return theta

#print(Black_call_value(6617, 6014.16, 0/365,(54/365), 0.033876, 0.259725))
#print(Black_call_Delta(6474.3, 6014.16, 0/365,(62/365), 0.033946, 0.25801))
#print(Black_call_Vega (6542,5972.418,0/365,(90/365),0.033737,0.13878))
#print(Black_call_Theta(6542,5972.418,0/365,(90/365),0.033737,0.13878))