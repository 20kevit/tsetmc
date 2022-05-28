from ..tools import get, hEven_to_time, dEven_to_date
import pandas as pd

BASE_URL = "http://cdn.tsetmc.com/api/"
__all__ = ["all_index", "info", "last_day", "history", "companies"]

def all_index():
    response = get(BASE_URL + "StaticData/GetStaticData")
    result = pd.DataFrame(dict(response.json())["staticData"])
    result.description = result.description.apply(str.strip)
    return result.drop("name", axis=1)

def info(insCode:str|int):
    response = get(BASE_URL + f"Instrument/GetInstrumentInfo/{insCode}")
    return dict(response.json())["instrumentInfo"]

def last_day(insCode:str|int):
    response = get(BASE_URL + f"Index/GetIndexB1LastDay/{insCode}")
    List = dict(response.json())["indexB1"]
    DATA = {}
    for l in List:
        time = hEven_to_time(l["hEven"])
        DATA[time] = {
            "value": l["xDrNivJIdx004"],
            "low": l["xPbNivJIdx004"],
            "high": l["xPhNivJIdx004"],
            "change": l["xVarIdxJRfV"]
        }

    return pd.DataFrame(DATA).transpose()

def history(insCode:str|int):
    response = get(BASE_URL + f"Index/GetIndexB2History/21948907150049163")
    List = dict(response.json())["indexB2"]
    DATA = {}
    for l in List:
        date = dEven_to_date(l["dEven"])
        DATA[date] = {
            "value" : l["xNivInuClMresIbs"],
            "low" : l["xNivInuPbMresIbs"],
            "high" : l["xNivInuPhMresIbs"],
        }
    return pd.DataFrame(DATA).transpose()

def companies(insCode:str|int):
    response = get(BASE_URL + f"ClosingPrice/GetIndexCompany/{insCode}")
    List = dict(response.json())["indexCompany"]
    DATA = {}
    for l in List:
        num_id = l["insCode"]
        DATA[num_id] = {
            "symbol": l["instrument"]["lVal18AFC"],
            "name": l["instrument"]["lVal30"],
            "close": l["pClosing"],
            "last": l["pDrCotVal"],
            "high": l["priceMax"],
            "low": l["priceMin"],
            "yesterday": l["priceYesterday"],
            "trade_value": l["qTotCap"],
            "trade_volume": l["qTotTran5"],
            "trade_count": l["zTotTran"]
        }