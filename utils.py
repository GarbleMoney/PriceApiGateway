# coding = utf-8
import json
import random
import requests

req_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}

token_whitelist = {
    'trx': ['gateio', 'ftx', 'kucoin'],
    'jst': ['gateio', 'kucoin'],
    'usdd': ['gateio'],
    'usdj': [],
    'usdc': []
}

def send_gateio_request(token_1):
    try:
        req = requests.get('https://data.gateapi.io/api2/1/ticker/{}_{}'.format(token_1, 'usdt'), headers=req_headers)
        api_ret = json.loads(req.content)
        ret_dict = {'status': 'success', 'price': None, 'description': 'gateio'}
        if 'last' in api_ret:
            ret_dict['price'] = float(api_ret['last'])
        return ret_dict
    except Exception as e:
        return {'status': 'error', 'description': str(e)}

def send_ftx_request(token_1):
    try:
        req = requests.get('https://colorlessgreenumbralla.com/api/markets/{}/{}/candles/last?resolution=300'.format(token_1, 'usdt'), headers=req_headers)
        api_ret = json.loads(req.content)
        ret_dict = {'status': 'success', 'price': None, 'description': 'ftx'}
        if 'result' in api_ret and 'close' in api_ret['result']:
            ret_dict['price'] = float(api_ret['result']['close'])
        return ret_dict
    except Exception as e:
        return {'status': 'error', 'description': str(e)}

def send_kucoin_request(token_1):
    try:
        pair_uppercase = '{}-{}'.format(token_1.upper(), 'USDT')
        req = requests.get('https://www.kucoin.com/_api/quicksilver/universe-currency/symbols/info/{}?coin={}&symbol={}&source=WEB&lang=en_US'.format(token_1, token_1, pair_uppercase), headers=req_headers)
        api_ret = json.loads(req.content)
        ret_dict = {'status': 'success', 'price': None, 'description': 'kucoin'}
        if 'success' in api_ret and api_ret['success']:
            if 'data' in api_ret and 'priceLiveData' in api_ret['data'] and 'close' in api_ret['data']['priceLiveData']:
                ret_dict['price'] = api_ret['data']['priceLiveData']['close']
            else:
                ret_dict['status'] = 'error'
                ret_dict['description'] = 'kucoin not supports this pair'
        else:
            ret_dict['status'] = 'error'
            ret_dict['description'] = 'kucoin returns bad status'
        return ret_dict
    except Exception as e:
        return {'status': 'error', 'description': str(e)}

def fetch_token_price(token):
    token = token.lower()
    supported_cex = ['gateio', 'ftx', 'kucoin']
    if token in token_whitelist:
        supported_cex = token_whitelist[token]
    if len(supported_cex) == 0:
        return {'status': 'error', 'description': 'token not supported'}
    choice = random.choice(supported_cex)
    statement = 'send_{}_request(\'{}\')'.format(choice, token)
    return eval(statement)
    
if __name__ == '__main__':
    print(fetch_token_price('trx'))

    print(send_gateio_request('usdd'))
    print(send_ftx_request('trx'))
    print(send_kucoin_request('trx'))
