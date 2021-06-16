import alpaca_trade_api.rest

import secrets
import alpaca_trade_api as tradeapi
from math import floor


"""
The purpose of this file is to create a common connection api that can connect to multiple brokers
"""

# This should be pulled from an ini file or something
broker_type = "alpaca"


class Broker:
    def __init__(self):
        self.cash = 0
        self.assets = []
        self.broker_vendor = "Default"


class AlpacaBroker(Broker):
    def __init__(self):
        super().__init__()
        self.broker_vendor = "Alpaca"
        self.api = tradeapi.REST(secrets.paper_key, secrets.paper_secret,
                                 secrets.paper_base, 'v2')
        self.get_cash()
        self.get_assets()

    def buy_stock(self, ticker, amount):
        if self.get_stock_info(ticker)["tradable"]:
            self.api.submit_order(symbol=ticker, qty=amount, side="buy", type="market", time_in_force="day")
            print(f"Order submitted for {amount} shares of {ticker}")

    def buy_dollar(self, ticker, amount):
        info = self.get_stock_info(ticker)
        if info["fractionable"] and info["tradable"]:
            self.api.submit_order(symbol=ticker, notional=amount, side="buy", type="market", time_in_force="day")
            print(f"Order submitted for ${amount} of {ticker}")
        elif self.get_stock_info(ticker)["tradable"]:
            # calculate amount of shares and round down
            shares = floor(amount / info["price"])
            self.api.submit_order(symbol=ticker, qty=shares, side="buy", type="market", time_in_force="day")
            print(f"Order submitted for {shares} of {ticker} -- not fractionable")

    def sell_stock(self, ticker, amount, close=False):
        #check position and close if appropriate
        try:
            position = float(self.api.get_position(ticker).qty)
        except alpaca_trade_api.rest.APIError:
            print(f"No position exists for {ticker}")
            return None
        assert type(amount) != str
        if amount >= position or close:
            self.api.close_position(ticker)
            print(f"Closing position {ticker}")
        elif amount > 0:
            # Could cause issues if amount is a fraction on a non fractional
            self.api.submit_order(symbol=ticker, qty=amount, side="sell", type="market", time_in_force="day")
            print(f"Order submitted to sell {amount} of {ticker}")
        else:
            print("Amount invalid")

    def sell_dollar(self, ticker, amount, close=False):
        #check position and close if appropriate
        try:
            position = float(self.api.get_position(ticker).market_value)
        except alpaca_trade_api.rest.APIError:
            print(f"No position exists for {ticker}")
            return None
        assert type(amount) != str
        if amount >= position or close:
            self.api.close_position(ticker)
            print(f"Closing position {ticker}")
        elif amount > 0:
            # Could cause issues if amount is a fraction on a non fractional
            self.api.submit_order(symbol=ticker, notional=amount, side="sell", type="market", time_in_force="day")
            print(f"Order submitted to sell {amount} of {ticker}")
        else:
            print("Amount invalid")

    def get_cash(self):
        self.cash = round(float(self.api.get_account().cash), 2)
        # print(self.cash)

    def get_assets(self):
        self.assets = []
        for symbol in self.api.list_positions():
            self.assets.append(symbol.symbol)
        # print(self.assets)

    def get_stock_info(self, ticker):
        last_price = self.api.get_last_trade(ticker)
        last_price = last_price.price

        asset_info = self.api.get_asset(ticker)
        fractionable = asset_info.fractionable
        name = asset_info.name
        tradable = asset_info.tradable
        exchange = asset_info.exchange

        asset_dict = {
            "name": name,
            "exchange": exchange,
            "tradable": tradable,
            "fractionable": fractionable,
            "price": last_price,
        }

        return asset_dict


broker = AlpacaBroker()
# print(broker.get_stock_info("AAPL"))
# print(broker.get_stock_info("AAPL")['tradable'] is True)
# broker.sell_dollar("QQQ", 100000000)
# broker.get_assets()
# broker.get_cash()
