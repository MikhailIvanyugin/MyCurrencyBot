import requests
import json

class ConvertionException(Exception):
    pass

class Convertor:
    @staticmethod
    def get_price(amount, quote, base):
        new_request = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={quote}&tsyms={base}")
        new_response = json.loads(new_request.content)[base]
        new_response_totals = round((new_response * float(amount)), 2)
        return new_response_totals
