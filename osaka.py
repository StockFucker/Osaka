#!/usr/bin/python2
#coding: utf-8 

from __future__ import division

from selector import select
from trader import trader
import time

class smallCapStock:
    def __init__(self, target_num=10):
        ''' 当日全部股票 '''
        self.trader = trader()
        holding_stocks = self.trader.holding.keys()
        self.sell_out([i for i in holding_stocks if i not in target_stocks])
        self.sell_out([i for i in holding_stocks if i not in target_stocks], first=False)
    
    def adjust(self):
        # 10支最小市值股票 
        target_stocks_info = select()
        print(target_stocks_info)
        # 目标股票
        # target_stocks = target_stocks_info.keys()
        # 持仓股票

        # # 清仓 
        # # 开仓
        # self.buy_in([i for i in target_stocks if i not in holding_stocks])

        # # 再次清仓, 针对雪球1% 无法清仓的情况调整

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
    while True:
        scs.adjust()
        time.sleep(5) 
