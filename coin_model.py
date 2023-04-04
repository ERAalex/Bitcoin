from requests import Session
import environ
import json
from db_app import TableWork

env = environ.Env()
environ.Env.read_env()
db_work = TableWork()


class CoinRequest:

    def __init__(self, token):
        self.token = token
        self.session = Session()
        self.headers = {
          'Accepts': 'application/json',
          'X-CMC_PRO_API_KEY': self.token,
        }

    def get_bitcoin(self):
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        params = {
          'start': '1',
          'limit': '1',
          'convert': 'USD',
        }

        self.session.headers.update(self.headers)
        response = self.session.get(url, params=params)
        data = json.loads(response.text)
        currence_name = data['data'][0]['name']
        currence_usd_price = data['data'][0]['quote']['USD']['price']

        changes = db_work.save_statics(currence_name, currence_usd_price)

        currence_data = {}
        currence_data[currence_name] = str(currence_usd_price) + ' $, ' + ' ' + 'цена изменилась на ' + str(changes)

        return currence_data

    def get_etherium(self):
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        params = {
          'start': '2',
          'limit': '1',
          'convert': 'USD',
        }

        self.session.headers.update(self.headers)
        response = self.session.get(url, params=params)
        data = json.loads(response.text)
        currence_name = data['data'][0]['name']
        currence_usd_price = data['data'][0]['quote']['USD']['price']

        changes = db_work.save_statics(currence_name, currence_usd_price)

        currence_data = {}
        currence_data[currence_name] = str(currence_usd_price) + ' $, ' + ' ' + 'цена изменилась на ' + str(changes)

        return currence_data
