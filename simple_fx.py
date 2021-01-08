import requests
from credentials import *

# create a rest client object
class Simple_FX_Client(object):
    def __init__(self, api_key=None, api_secret=None,\
            account=None, reality=None):

        self.api_key = api_key
        self.api_secret = api_secret
        self.account = account
        self.reality = reality
        self.url = 'https://rest.simplefx.com'
        self.headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
                }


    # get a list of instruments
    def list_instruments(self):
        url = 'https://simplefx.com/utils/instruments.json'
        response = requests.get(url, headers=self.headers)
        data = response.json()
        data = list(data.values())
        return data

    
    # get symbol information
    def symbol_info(self, symbol):
        symbol_list = self.list_instruments()

        for i in symbol_list:
            data = i.get('symbol')

            if data == symbol:
                data = i

                return data


    # get authentication token
    def auth_key(self):
        options = {'clientId':self.api_key, 'clientSecret':self.api_secret}
        url = self.url + '/api/v3/auth/key'
        response = requests.post(url, headers=self.headers, json=options)
        json_response = response.json()
        token = json_response['data']
        token = token['token']
        return token


    # get overview of all accounts
    def accounts_overview(self):
        self.headers['Authorization'] = self.auth_key()
        url = self.url + '/api/v3/accounts'
        response = requests.get(url, headers=self.headers)
        data = response.json()
        return data


    # get status of of individual account
    def account_status(self):
        self.headers['Authorization'] = self.auth_key()
        url = self.url + '/api/v3/accounts/{}/{}'.format(
                self.reality, self.account)

        response = requests.get(url, headers=self.headers)
        data = response.json()
        return data


    # place a market order
    def market_order(self, symbol, side, vol, tp=None, sl=None): 
        self.headers['Authorization'] = self.auth_key()
        url = self.url + '/api/v3/trading/orders/market'
        options = {
                "Reality":self.reality,
                "Login":self.account,
                "Symbol":symbol,
                "Side":side,
                "Volume":vol,
                "RequestId":"string"
                }

        if tp is not None:
            options['TakeProfit'] = tp

        if sl is not None:
            options['StopLoss'] = sl

        response = requests.post(url, headers=self.headers, json=options)
        data = response.json()
        return data


    # place a pending order
    def pending_order(self, symbol, side, price, vol, tp=None, sl=None):
        self.headers['Authorization'] = self.auth_key()
        url = self.url + '/api/v3/trading/orders/pending'
        options = {
                "Reality":self.reality,
                "Login":self.account,
                "Symbol":symbol,
                "ActivationPrice":price,
                "Volume":vol,
                "Side":side,
                "RequestId":"string",
                }

        if tp is not None:
            options['TakeProfit'] = tp

        if sl is not None:
            options['StopLoss'] = sl

        response = requests.post(url, headers=self.headers, json=options)
        data = response.json()
        return data


    # adjust a pending order
    def adjust_order(self, order_id, price, vol, tp=None, sl=None):
        self.headers['Authorization'] = self.auth_key()
        url = self.url + '/api/v3/trading/orders/pending'
        options = {
                "Reality":self.reality,
                "Login":self.account,
                "Id":order_id,
                "ActivationPrice":price,
                "Volume":vol,
                "RequestId":"string",
                }

        if tp is not None:
            options['TakeProfit'] = tp

        if sl is not None:
            options['StopLoss'] = sl

        response = requests.put(url, headers=self.headers, json=options)
        data = response.json()
        return data


    # adjust take profit order
    def adjust_tp(self, order_id, tp):
        self.headers['Authorization'] = self.auth_key()
        url = self.url + '/api/v3/trading/orders/market'
        
        options = {
                "Login":572389,
                "Reality":"DEMO",
                "Id":order_id,
                "TakeProfit":tp
                }

        response = requests.put(url, headers=self.headers, json=options)
        data = response.json()
        return data
            

    # adjust stop loss order
    def adjust_sl(self, order_id, sl):
        self.headers['Authorization'] = self.auth_key()
        url = self.url + '/api/v3/trading/orders/market'
        
        options = {
                "Login":self.account,
                "Reality":self.reality,
                "Id":order_id,
                "StopLoss":sl
                }

        response = requests.put(url, headers=self.headers, json=options)
        data = response.json()
        return data


    # delete a pending order
    def delete_order(self, order_id):
        self.headers['Authorization'] = self.auth_key()
        url = self.url + '/api/v3/trading/orders/pending'
        options = {
                "Login":self.account,
                "Reality":self.reality,
                "Id":order_id,
                "RequestId":"string",
                }

        response = requests.delete(url, headers=self.headers, json=options)
        data = response.json()
        return data


    # close an open position
    def close_position(self, order_id, vol):
        self.headers['Authorization'] = self.auth_key()
        url = self.url + '/api/v3/trading/orders/market'
        options = {
                "Login":self.account,
                "Reality":self.reality,
                "Id":order_id,
                "Volume":vol,
                "RequestId":"string",
                }

        response = requests.delete(url, headers=self.headers, json=options)
        data = response.json()
        return data


    # get positions and pending orders
    def get_positions(self):
        self.headers['Authorization'] = self.auth_key()
        url = self.url + '/api/v3/trading/orders/active'
        options = {
                "Login":self.account,
                "Reality":self.reality,
                }

        response = requests.post(url, headers=self.headers, json=options)
        data = response.json()
        return data


client = Simple_FX_Client(api, secret, account, reality)
