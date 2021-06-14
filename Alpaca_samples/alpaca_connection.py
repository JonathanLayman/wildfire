import secrets
import alpaca_trade_api as tradeapi

key = secrets.paper_key
secret = secrets.paper_secret
base = secrets.paper_base
api = tradeapi.REST(key, secret, base, 'v2')
account = api.get_account()
print(account.status)
