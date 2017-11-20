# !/usr/bin/env python
# encoding: utf-8
import sys
import os
import pandas as pd

def reverse_direction_if_close(row):
    if row.open_close == 0:
        return row.direction
    return 0 if row.direction == 1 else 1

def daily_position_from_trancation(df):
    # 如果是开仓则数量为正数,平仓则数量为负数
    df['position_effect'] = df.apply(lambda x : x.lots if x.open_close == 0 else -x.lots, axis=1)
    # 将平仓订单的方向改为相反方向,用来计算持仓
    df['direction_for_position'] = df.apply(reverse_direction_if_close, axis=1)
    df.reset_index(inplace=True)

    instruments = df.instrument.unique().tolist()
    series_list = []
    for instrument in instruments:#按合约划分
        for direction in range(2):#direction = 0/1
            series = df[(df.instrument == instrument) & (df.direction_for_position == direction)]['position_effect'].cumsum()#把该合约的挑出来，把同个方向的挑出来
            series_list.append(series)
            df['position_cumsum'] = pd.concat(series_list).sort_index()
    return df.groupby(['real_trade_date','instrument', 'direction_for_position' ])['position_cumsum'].last()

#?????????????????????????????????????????????????????????