import requests
import time
from datetime import datetime

class gecko:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.url = "https://api.coingecko.com/api/v3/{call}"

# ASSIGN API KEY.
    def set_api_key(self, api_key):
        self.api_key = api_key

# /ping - CHECK API SERVER STATUS.
    def ping(self):
        url_formatted = self.url.format(call="ping")
        response = requests.get(url_formatted)
        data = response.json()
        return data

# /simple/price - GET THE CURRENT PRICE OF ANY CRYPTOCURRENCIES IN ANY OTHER SUPPORTED CURRENCIES THAT YOU NEED.
    def get_current_price(self, coins, fiat='usd', include_market_cap='false', include_24hr_vol='false', include_24hr_change='false', include_last_updated_at='false'):
        if(type(coins) == list):
            coins = '%2C'.join(coins)

        if(type(fiat) == list):
            fiat = '%2C'.join(fiat)

        call = "simple/price" + \
                f"?ids={coins}" + \
                f"&vs_currencies={fiat}" + \
                f"&include_market_cap={include_market_cap}" + \
                f"&include_24hr_vol={include_24hr_vol}" + \
                f"&include_24hr_change={include_24hr_change}" + \
                f"&include_last_updated_at={include_last_updated_at}"

        url_formatted = self.url.format(call=call)
        
        response = requests.get(url_formatted)
        data = response.json()
        return data

# /coins/{id}/market_chart/range - GET HISTORICAL MARKET DATA INCLUDE PRICE, MARKET CAP, AND 24H VOLUME WITHIN A RANGE OF TIMESTAMP (GRANULARITY AUTO).
    def get_market_chart_range(self, coin, startDate, endDate, fiat='usd'):
        startDate_UNIX = time.mktime(datetime.strptime(startDate, "%Y-%m-%d").timetuple())
        endDate_UNIX = time.mktime(datetime.strptime(endDate, "%Y-%m-%d").timetuple())

        call = f"coins/{coin}/market_chart/range" + \
                f"?vs_currency={fiat}" + \
                f"&from={startDate_UNIX}" + \
                f"&to={endDate_UNIX}"
        
        url_formatted = self.url.format(call=call)

        response = requests.get(url_formatted)
        data = response.json()
        return data