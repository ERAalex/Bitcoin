from coin_model import CoinRequest
from db_app import Cryptocurrency, TableWork
import environ
from time import sleep

env = environ.Env()
environ.Env.read_env()

getmoney = CoinRequest(env('CMC_PRO_API_KEY'))
db_work = TableWork()


while True:
    print(getmoney.get_etherium())
    sleep(1)
    print(getmoney.get_bitcoin())
    sleep(5)
