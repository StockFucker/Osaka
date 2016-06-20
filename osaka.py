#!/usr/bin/python2
#coding: utf-8 

from __future__ import division

# from selector import select
from trader import trader
import pandas as pd
import easyquotation 

def stockFilter(stock):
        head = stock[:1]
        return head == "0" or head == "3" or head == "6"

class smallCapStock:
    def __init__(self, target_num=10):
        ''' 当日全部股票 '''
        quotation = easyquotation.use('qq')
        self.stocks_info = quotation.all
        self.target_num = target_num
        # self.trader = trader()

    def min_volume_stocks(self):

        df = pd.DataFrame(self.stocks_info).T
        to_drop = list(df.columns)
        to_drop.remove("now")
        to_drop.remove("涨跌(%)")
        to_drop.remove("总市值")
        to_drop.remove("name")
        to_drop.remove("unknown")
        df = df.drop(pd.Index(to_drop),1)
        stocks = filter(stockFilter,list(df.index))
        df = df[df.index.isin(stocks) == True] 
        df.columns = ["name","price","unknown","total_value","changepercent"]
        print(df)
        # return d f, sort_stocks[self.target_num]

    def adjust(self):
        # 10支最小市值股票 
        target_stocks_info, target_add_stock = self.min_volume_stocks()
        # 目标股票
        # target_stocks = target_stocks_info.keys()
        # 持仓股票
        # holding_stocks = self.trader.holding.keys()

        # # 清仓 
        # self.sell_out([i for i in holding_stocks if i not in target_stocks])
        # # 开仓
        # self.buy_in([i for i in target_stocks if i not in holding_stocks])

        # # 再次清仓, 针对雪球1% 无法清仓的情况调整
        # self.sell_out([i for i in holding_stocks if i not in target_stocks], first=False)

        # # 剩余余额买target_num+1标的
        # self.buy_in([target_add_stock.get('code')], first=False)

    def sell_out(self, stocks, first=True):
        ''' 清仓
            first 针对雪球1%无法清仓的情况对应处理
        '''
        if not first:
            # 重新获取交易信息
            self.trader = trader()
        for stock in stocks:
            amount = self.trader.holding.get(stock).get('enable_amount') or 0
            if not first or (first and amount > 100):
                current_price = float(self.stocks_info.get(stock).get('now'))
                trade_price = float(current_price) - 0.01
                self.trader.sell(stock, amount, current_price)

    def buy_in(self, stocks, first=True):
        ''' 开仓 
            first 针对剩余金额全部购买一支标的进行处理
        '''
        if not first:
            # 重新获取交易信息
            self.trader = trader()
        # 账户可用余额
        enable_balance = self.trader.enable_balance
        #print self.trader.balance
        for stock in stocks:
            current_price = float(self.stocks_info.get(stock).get('now'))
            amount = int(enable_balance/self.target_num/current_price/100) * 100 if first else\
                    int(enable_balance/current_price/100) * 100
            if amount>=100:
                self.trader.buy(stock, amount, current_price)

if __name__ == '__main__':
    scs = smallCapStock()
    scs.adjust()