import secrets
import alpaca_trade_api as tradeapi

key = secrets.paper_key
secret = secrets.paper_secret
base = secrets.paper_base
api = tradeapi.REST(key, secret, base, 'v2')
account = api.get_account()
# print(account.status)


# Get price of an asset
def get_asset_price(asset):
    info = api.get_last_trade(asset)
    print(info.price)


# Create a buy order
def buy_or_sell(asset, dollars, amount, side, _type="market", time_in_force="day"):
    if side == "buy" or side == "sell":
        if dollars:
            api.submit_order(symbol=asset, notional=amount, side=side, type=_type, time_in_force=time_in_force)
        else:
            api.submit_order(symbol=asset, qty=amount, side=side, type=_type, time_in_force=time_in_force)
    else:
        print("error side must be 'buy' or 'sell'")


# get info on assets
def get_info_on_assets():
    api.list_assets()


sym = "AAPL"
print(f"Getting price for {sym}")
get_asset_price("AAPL")
print(f"Buy order for 1 share of {sym}")
buy_or_sell(asset=sym, dollars=False, amount=1, side='buy')
print(f"Buy $100 of {sym}")
buy_or_sell(asset=sym, dollars=True, amount=100, side='buy')
print(f"list assets")
get_info_on_assets()
