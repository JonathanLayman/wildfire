import secrets
import alpaca_trade_api as tradeapi
from math import floor

key = secrets.paper_key
secret = secrets.paper_secret
base = secrets.paper_base
api = tradeapi.REST(key, secret, base, 'v2')
account = api.get_account()
# print(account.status)
# https://github.com/alpacahq/alpaca-trade-api-python/blob/master/alpaca_trade_api/rest.py


# Get price of an asset
def get_asset_price(asset):
    info = api.get_last_trade(asset)
    print(info.price)


# Create a buy order
def buy_or_sell(asset, dollars, amount, side, _type="market", time_in_force="day"):
    if side == "buy" or side == "sell":
        if dollars:
            # Check if asset is fractionable
            if api.get_asset(asset).fractionable:
                api.submit_order(symbol=asset, notional=amount, side=side, type=_type, time_in_force=time_in_force)
            else:
                # grab leftover cash
                shares = floor(amount / api.get_last_trade(asset).price)
                print(f"Buying {shares} shares of {asset} because it is not fractional")
                api.submit_order(symbol=asset, qty=shares, side=side, type=_type, time_in_force=time_in_force)
        else:
            api.submit_order(symbol=asset, qty=amount, side=side, type=_type, time_in_force=time_in_force)
    else:
        print("error side must be 'buy' or 'sell'")


# get info on assets
def get_info_on_assets():
    api.list_assets()
    api.list_positions()


# sym = "QQQ"
# print(api.get_asset(sym))
# if api.get_asset(sym).fractionable == False:
#     print("here")
# buy_or_sell(asset=sym, dollars=True, amount=5000, side='buy')

# sym = "AAPL"
# print(f"Getting price for {sym}")
# get_asset_price("AAPL")
# print(f"Buy order for 1 share of {sym}")
# buy_or_sell(asset=sym, dollars=False, amount=1, side='buy')
# print(f"Buy $100 of {sym}")
# buy_or_sell(asset=sym, dollars=True, amount=100, side='buy')
# print(f"list assets")
# get_info_on_assets()
