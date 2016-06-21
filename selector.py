#!/usr/bin/python
# coding:utf8
# return all stocks information include price and voloum, excluding ST and risk notification stocks

import pandas as pd
import easyquotation

def get_prices():
    quotation = easyquotation.use('qq')
    stocks_info = quotation.all
    return stocks_info

def stockFilter(stock):
        head = stock[:1]
        return head == "0" or head == "3" or head == "6"

def select():
    stocks_info = get_prices()
    df = pd.DataFrame(stocks_info).T
    print(df.columns)
    to_drop = list(df.columns)
    for i in range(1,6):
        to_drop.remove("ask" + str(i))
        to_drop.remove("bid" + str(i))
    to_drop.remove("close")
    to_drop.remove("turnover")
    to_drop.remove("unknown")
    to_drop.remove("涨停价")
    to_drop.remove("涨跌(%)")
    to_drop.remove("跌停价")
    to_drop.remove("总市值")
    df = df.drop(pd.Index(to_drop),1)
    stocks = filter(stockFilter,list(df.index))
    df = df[df.index.isin(stocks) == True]
    columns = list(df.columns)[:13]
    columns.extend(["total_value","high_limit","change_percent","low_limit"])
    df.columns = columns
    return df

if __name__ == '__main__':
    print(select())
