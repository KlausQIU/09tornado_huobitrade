#coding=utf-8

import urllib
import hashlib
import hmac
import base64
import sys
import os
append_path =  os.path.dirname(os.getcwd())
sys.path.append(append_path)
# from handlers.data_collection import db as d

#在此输入您的Key
ACCESS_KEY="7ffd4f94-63d605e6-d5f400fb-a6ba0"
SECRET_KEY="d5d52f33-dcbd2167-5c6b7b0f-f5676"

HUOBI_SERVICE_API="https://api.huobi.com/apiv3"

BUY = "buy"
BUY_MARKET = "buy_market"
CANCEL_ORDER = "cancel_order"
ACCOUNT_INFO = "get_account_info"
NEW_DEAL_ORDERS = "get_new_deal_orders"
ORDER_ID_BY_TRADE_ID = "get_order_id_by_trade_id"
GET_ORDERS = "get_orders"
ORDER_INFO = "order_info"
SELL = "sell"
SELL_MARKET = "sell_market"

def signature(params):
    params = sorted(params.iteritems(), key=lambda d:d[0], reverse=False)
    message = urllib.urlencode(params)
    m = hashlib.md5()
    m.update(message)
    m.digest()
    sig=m.hexdigest()
    return sig

