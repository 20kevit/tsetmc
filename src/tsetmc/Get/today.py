from bs4 import BeautifulSoup
import pandas as pd
import datetime
from .. import base
from ..tools import get
from .__init__ import __BASE_URL__

__all__ = ["general", "candles", "trades", "real_legal", "holders"]

def general(num_id: int | str) -> dict:
    response = get(
        __BASE_URL__ + f"tsev2/data/instinfodata.aspx?i={num_id}&c=39%20")
    if response.text == "":
        print("no data for ", num_id)
        return
    values = response.text.split(";")
    result = {}

    # Basics:
    
    primary = values[0].split(",")
    result["last_time_update"] = primary[0]
    result["last"] = primary[2]
    result["close"] = primary[3]
    result["first"] = primary[4]
    result["yesterday"] = primary[5]
    result["low"] = primary[6]
    result["high"] = primary[7]
    result["trade_count"] = primary[8]
    result["volume"] = primary[9]
    result["value"] = primary[10]

    # base.orders:
    base.orders = values[2].split(",")[:-1]
    asks = []
    bids = []
    for row in base.orders:
        items = row.split("@")
        asks.append(base.order(items[0], items[1], items[2]))
        bids.append(base.order(items[5], items[4], items[3]))

    result["asks"] = asks
    result["bids"] = bids

    # Real and Legal person Data:

    RL = values[4].split(",")
    if len(RL) == 10:
        result["RL_data"] = {
            "real_person": {
                "buy": {
                    "volume": RL[0],
                    "count": RL[5]
                },
                "sell": {
                    "volume": RL[3],
                    "count": RL[8]
                }
            },
            "legal_person": {
                "buy": {
                    "volume": RL[1],
                    "count": RL[6]
                },
                "sell": {
                    "volume": RL[4],
                    "count": RL[9]
                }
            }
        }
    else:
        result["RL_data"] = None
    return result

def candles(num_id: int | str) -> pd.DataFrame:
    response = get(
        __BASE_URL__ + f"tsev2/chart/data/IntraDayPrice.aspx?i={num_id}")
    
    data = response.text.split(";")
    times = []
    for i in range(len(data)):
        data[i] = data[i].split(",")
        times.append(data[i][0])
        data[i] = data[i][1:]

    result = pd.DataFrame(
        data, times, ["high", "low", "open", "close", "volume"])
    return result

def trades(num_id: int | str) -> pd.DataFrame:
    page = get(
        __BASE_URL__ + f"tsev2/data/TradeDetail.aspx?i={num_id}")
    if "Error" in page.text:
        print("Internal Server Error")
        return None
    
    soup = BeautifulSoup(page.content, "html.parser")
    rows = soup.find_all(name="row")

    data = {}
    for row in rows:
        cells = row.find_all(name="cell")
        
        time = cells[1].text
        hour, minute, second = time.split(":")
        time = datetime.time(int(hour), int(minute), int(second))
        
        volume = int(cells[2].text)
        price = int(float(cells[3].text))
        
        data[time] = {
            "volume": volume,
            "price": price
        }

    return pd.DataFrame(data).transpose()

def real_legal(num_id: int | str) -> dict:
    response = get(__BASE_URL__ + f"tsev2/data/clienttype.aspx?i={num_id}")
    
    data = response.text.split(";")

    result = {}
    for row in data:
        values = row.split(",")
        time = values[0]
        year = int(time[:4])
        month = int(time[4:6])
        day = int(time[-2:])
        time = datetime.date(year, month, day)

        result[time] = {
            "count": {
                "buy": {
                    "real": int(values[1]),
                    "legal": int(values[2])
                },
                "sell": {
                    "real": int(values[3]),
                    "legal": int(values[4])
                }
            },
            "volume": {
                "buy": {
                    "real": int(values[5]),
                    "legal": int(values[6])
                },
                "sell": {
                    "real": int(values[7]),
                    "legal": int(values[8])
                }
            },
            "value": {
                "buy": {
                    "real": int(values[9]),
                    "legal": int(values[10])
                },
                "sell": {
                    "real": int(values[11]),
                    "legal": int(values[12])
                }
            }
        }

    return result

def holders(code: str) -> list[dict]:
    page = get(__BASE_URL__ + f"Loader.aspx?Partree=15131T&c={code}")
    if "Error" in page.text:
        print("Internal Server Error")
        return None
    
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find(name="tbody")
    rows = table.find_all(name="tr")

    result = []

    for row in rows:
        code = row.get_attribute_list("onclick")[0].split("'")[1].split(",")[0]

        td = row.find_all(name="td")
        name = td[0].text

        try:
            share = td[1].find(name="div").get_attribute_list("title")[0]
        except:
            share = td[1].text
        share = int(share.replace(",", ""))
        percent = float(td[2].text)

        try:
            change = td[3].find(name="div").get_attribute_list("title")[0]
        except:
            change = td[3].text
        change = int(change.replace(",", "")) * -1

        result.append(
            {
                "code": code,
                "name": name,
                "share": share,
                "percent": percent,
                "change": change
            }
        )

    return result
