import pandas as pd
import datetime
from ..tools import get, date_to_dEven, hEven_to_time
from .__init__ import __BASE_URL__

class Day:
    def __init__(self, date: datetime.date):
        self.dEven = date_to_dEven(date)
        
    def closing_price(self, num_id: int | str):
        return closing_price(num_id, self.dEven)
        
    def trades(self, num_id: int | str):
        return trades(num_id, self.dEven)
    
    def instrument(self, num_id: int | str):
        return instrument(num_id, self.dEven)
    
    def client_type(self, num_id: int | str):
        return client_type(num_id, self.dEven)
    
    def general(self, num_id: int | str):
        return general(num_id, self.dEven)

def closing_price(num_id: int | str, dEven:str) -> pd.DataFrame:
    response = get(
        f"http://cdn.tsetmc.com/api/ClosingPrice/GetClosingPriceHistory/{num_id}/{dEven}")
    data = dict(response.json())['closingPriceHistory']

    result = {}
    for item in data[::-1]:
        time = hEven_to_time(item["hEven"])
        closing_price = int(float(item['pClosing']))
        last_price = int(float(item['pDrCotVal']))
        trades_count = int(float(item['zTotTran']))
        volume = int(float(item['qTotTran5J']))
        value = int(float(item['qTotCap']))

        result[time] = {
            "Close": closing_price,
            "Last": last_price,
            "Count": trades_count,
            "Volume": volume,
            "Value": value
        }

    return pd.DataFrame(result).transpose()

def trades(num_id: int | str, dEven:str) -> pd.DataFrame:
    response = get(f"http://cdn.tsetmc.com/api/Trade/GetTradeHistory/{num_id}/{dEven}/false")
    data = dict(response.json())['tradeHistory']
    
    result = {}
    for item in data[::-1]:
        id = item["nTran"]
        time = hEven_to_time(item["hEven"])
        volume = item['qTitTran']
        price = item['pTran']
        canceled = bool(item['canceled'])
        
        result[id] = {
            "time": time,
            "volume": volume,
            "price": price,
            "canceled": canceled
        }
        
    return pd.DataFrame(result).transpose()

def instrument(num_id: int | str, dEven:str) -> dict:
    response = get(f"http://cdn.tsetmc.com/api/Instrument/GetInstrumentHistory/{num_id}/{dEven}")
    return dict(response.json())["instrumentHistory"]

def client_type(num_id: int | str, dEven:str):
    try:
        response = get(f"http://cdn.tsetmc.com/api/ClientType/GetClientTypeHistory/{num_id}/{dEven}")
    except:
        return
    
    data = dict(response.json())["clientType"]
    
    return {
        "buy": {
            "real": {
                "volume": data["buy_I_Volume"],
                "value": data["buy_I_Value"],
                "count": data["buy_I_Count"]
            },
            "legal": {
                "volume": data["buy_N_Volume"],
                "value": data["buy_N_Value"],
                "count": data["buy_N_Count"]
            }           
        },
        "sell": {
            "real": {
                "volume": data["sell_I_Volume"],
                "value": data["sell_I_Value"],
                "count": data["sell_I_Count"]
            },
            "legal": {
                "volume": data["sell_N_Volume"],
                "value": data["sell_N_Value"],
                "count": data["sell_N_Count"]
            } 
        }
    }
    
def general(num_id: int | str, dEven:str) -> dict:
    response = get(f"http://cdn.tsetmc.com/api/ClosingPrice/GetClosingPriceDaily/{num_id}/{dEven}")
    return dict(response.json())["closingPriceDaily"]

"""
def general(num_id: int | str, dEven:str) -> dict:
    response = get(f"http://cdn.tsetmc.com/api/MarketData/GetStaticThreshold/{num_id}/{dEven}")
    data = dict(response.json())["staticThreshold"]
"""