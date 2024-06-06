import requests
import random
import time
from paydb import *
import json
token = "token"
import random
import time
from datetime import timedelta
from fake_useragent import UserAgent
import requests
from paydb import *
shop_id = shopid
import json
def createpay(value,comment,userid):
    if value < 100:
        return ['До 100 рублей авто оплата не работает',123]
    id = f"{int(random.randint(0,6666666) + time.time())}"
    r = requests.post(f'https://lk.rukassa.is/api/v1/create?shop_id={shop_id}&order_id={id}&amount={value}&token={token}').json()
    true_id = r['id']
    add_pltej(r['id'],id,userid,comment)
    return [r['url'],true_id]
def checkpay(billid):
    state = requests.post(url = f"https://lk.rukassa.is/api/v1/getPayInfo?id={billid}&shop_id={shop_id}&token={token}").json()['status']
    if state == 'PAID':
        return True
    else:
        return False


