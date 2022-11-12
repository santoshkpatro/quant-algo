# from kiteconnect import KiteConnect
import requests
import hashlib
from django.conf import settings

class Kite:
    KITE_API_END_POINT = 'https://api.kite.trade'
    KITE_SESSION_END_POINT = 'https://api.kite.trade/session/token'


    def get_checksum(self, request_token):
        raw_text = settings.KITE_API_KEY.encode('utf-8') + request_token.encode('utf-8') + settings.KITE_API_SECRET.encode('utf-8')
        checksum = hashlib.sha256(raw_text).hexdigest()
        return checksum

    # def __init__(self):
        # self.kite_api_key = settings.KITE_API_KEY
        # self.kite_api_secret = settings.KITE_API_SECRET
        # checksum = self.get_checkum(request_token)
        # print(checksum)

        # headers = {
        #     'X-Kite-Version': '3'
        # }
        # params = {
        #     'api_key': settings.KITE_API_KEY,
        #     'request_token': request_token,
        #     'checksum': checksum
        # }
        # print(params)
        # # res = requests.post(
        # #     self.KITE_SESSION_END_POINT,
        # #     params=params,
        # #     headers=headers
        # # )

        # # print(res.json())

    def fetch(self, access_token):
        pass

