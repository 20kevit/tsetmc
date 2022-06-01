from bs4 import BeautifulSoup
import pandas as pd
import datetime as datetime
from ..tools import get, jalali_to_gregorian

__BASE_URL__ = "http://www.tsetmc.com/"
__all__ = ["basics", "statistics", "trade_history", "shares_change", "adjust_history",
           "status_changes", "ID", "codal_top_new", "all_tickers"]


def basics(num_id: int | str) -> dict:
    page = get(__BASE_URL__ + f"Loader.aspx?ParTree=151311&i={num_id}")
    if "Error" in page.text:
            print("Internal Server Error")
            return None
        
    soup = BeautifulSoup(page.content, "html.parser")
    values = soup.find_all(name="script")[4].text[4:-1].split(",")
    values = values[:-1] + values[-1].split(";")

    result = {}

    for v in values:
        key, value = v.split("=")
        if value[0] == "'":
            value = value[1:-1]
        try:
            value = int(value)
        except:
            try:
                value = float(value)
            except:
                if value == "":
                    value = None
        result[key] = value

    return result


def statistics(num_id: int | str) -> dict:
    response = get(
        "http://www.tsetmc.com/tsev2/data/instValue.aspx?i={num_id}&t=i")

    data = response.text.split(";")
    values = [None] + [int(item.split(",")[-1]) for item in data]

    return {
        "trades": {
            "value": {
                "average": {
                    "last3month": values[1],
                    "last12month": values[2]
                },
                "rank": {
                    "last3month": values[3],
                    "last12month": values[4]
                }
            },
            "volume": {
                "average": {
                    "last3month": values[5],
                    "last12month": values[6]
                },
                "rank": {
                    "last3month": values[7],
                    "last12month": values[8]
                }
            },
            "count": {
                "average": {
                    "last3month": values[9],
                    "last12month": values[10]
                },
                "rank": {
                    "last3month": values[11],
                    "last12month": values[12]
                }
            }
        },
        "last_day": {
            "weighted_average_price": {
                "without_basevol": values[13],
                "with_basevol": values[14]
            },

            "lastday_trade": {
                "value": values[15],
                "volume": values[16],
                "count": values[17]
            },
            "company_value": {
                "amount": values[36],
                "rank": values[37]
            }
        },
        "days": {
            "negative": {
                "count": {
                    "last3month": values[18],
                    "last12month": values[19]
                },
                "percent": {
                    "last3month": values[20],
                    "last12month": values[21]
                },
                "rank": {
                    "last3month": values[22],
                    "last12month": values[23]
                }
            },
            "without_trade_count": {
                "last3month": values[24],
                "last12month": values[25]
            },
            "positive": {
                "count": {
                    "last3month": values[26],
                    "last12month": values[27]
                },
                "percent": {
                    "last3month": values[28],
                    "last12month": values[29]
                },
                "rank": {
                    "last3month": values[30],
                    "last12month": values[31]
                }
            },
            "with_trade": {
                "count": {
                    "last3month": values[32],
                    "last12month": values[33]
                },
                "rank": {
                    "last3month": values[34],
                    "last12month": values[35]
                }
            },
            "open": {
                "count": {
                    "last3month": values[38],
                    "last12month": values[39]
                },
                "percent": {
                    "last3month": values[40],
                    "last12month": values[41]
                },
                "rank": {
                    "last3month": values[42],
                    "last12month": values[43]
                }
            },
            "close": {
                "count": {
                    "last3month": values[44],
                    "last12month": values[45]
                },
                "percent": {
                    "last3month": values[46],
                    "last12month": values[47]
                },
                "rank": {
                    "last3month": values[48],
                    "last12month": values[49]
                }
            }
        },
        "buy_volume": {
            "real": {
                "average": {
                    "last3month": values[50],
                    "last12month": values[51]
                },
                "rank": {
                    "last3month": values[52],
                    "last12month": values[53]
                }
            },
            "leagal": {
                "average": {
                    "last3month": values[54],
                    "last12month": values[55]
                },
                "rank": {
                    "last3month": values[56],
                    "last12month": values[57]
                }
            }
        },
        "buyers_count": {
            "real": {
                "average": {
                    "last3month": values[58],
                    "last12month": values[59]
                },
                "rank": {
                    "last3month": values[60],
                    "last12month": values[61]
                }
            },
            "leagal": {
                "average": {
                    "last3month": values[62],
                    "last12month": values[63]
                },
                "rank": {
                    "last3month": values[64],
                    "last12month": values[65]
                }
            },
            "average": {
                "last3month": values[66],
                "last12month": values[67]
            },
            "rank": {
                "last3month": values[68],
                "last12month": values[69]
            }
        },
        "sell_volume": {
            "real": {
                "average": {
                    "last3month": values[70],
                    "last12month": values[71]
                },
                "rank": {
                    "last3month": values[72],
                    "last12month": values[73]
                }
            },
            "leagal": {
                "average": {
                    "last3month": values[74],
                    "last12month": values[75]
                },
                "rank": {
                    "last3month": values[76],
                    "last12month": values[77]
                }
            }
        },
        "sellers_count": {
            "real": {
                "average": {
                    "last3month": values[78],
                    "last12month": values[79]
                },
                "rank": {
                    "last3month": values[80],
                    "last12month": values[81]
                }
            },
            "leagal": {
                "average": {
                    "last3month": values[82],
                    "last12month": values[83]
                },
                "rank": {
                    "last3month": values[84],
                    "last12month": values[85]
                }
            },
            "average": {
                "last3month": values[86],
                "last12month": values[87]
            },
            "rank": {
                "last3month": values[88],
                "last12month": values[89]
            }
        }
    }


def trade_history(num_id: int | str, adjust=False) -> pd.DataFrame:
    data = get(
        f"http://members.tsetmc.com/tsev2/data/InstTradeHistory.aspx?i={num_id}&Top=999999&A=0")
    data = data.text.split(";")[:-1]


    dates = []
    for i in range(len(data)):
        data[i] = data[i].split("@")

        new_date = data[i][0]
        Y, M, D = int(new_date[:4]), int(new_date[4:6]), int(new_date[6:])
        new_date = datetime.date(Y, M, D)
        dates.append(new_date)

        data[i] = list(map(float, data[i][1:]))
        data[i] = list(map(int, data[i]))

    result = pd.DataFrame(
        data = data[::-1],
        index = dates[::-1],
        columns = ["high", "low", "close", "last", "first", "yesterday", "value", "volume", "count"]
    )
    
    if(adjust):        
        adjusts = adjust_history(num_id)
        for date in adjusts.index:
            rate = adjusts.rate[date]
            result["high"][result.index < date] = result["high"][result.index < date].apply(lambda x: x*rate)
            result["low"][result.index < date] = result["low"][result.index < date].apply(lambda x: x*rate)
            result["close"][result.index < date] = result["close"][result.index < date].apply(lambda x: x*rate)
            result["last"][result.index < date] = result["last"][result.index < date].apply(lambda x: x*rate)
            result["first"][result.index < date] = result["first"][result.index < date].apply(lambda x: x*rate)
            result["yesterday"][result.index < date] = result["yesterday"][result.index < date].apply(lambda x: x*rate)
    
    return result


def share_changes(num_id: int | str) -> pd.DataFrame:
    page = get(
        __BASE_URL__ + f"Loader.aspx?Partree=15131H&i={num_id}")
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find(name="tbody")
    rows = table.find_all(name="tr")

    data = {}
    for row in rows:
        TDs = row.find_all(name="td")
        date = TDs[0].text

        new = TDs[1].find(name="div").get_attribute_list("title")[0]
        new = int(new.replace(",", ""))

        previous = TDs[2].find(name="div").get_attribute_list("title")[0]
        previous = int(previous.replace(",", ""))

        data[date] = {
            "previous":previous,
            "new": new
        }

    return pd.DataFrame(data).transpose()


def adjust_history(num_id: int | str) -> pd.DataFrame:
    page = get(
        __BASE_URL__ + f"Loader.aspx?Partree=15131G&i={num_id}")
    if "Error" in page.text:
            print("Internal Server Error")
            return pd.DataFrame(columns=["before", "after", "rate"])
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find(name="tbody")
    rows = table.find_all(name="tr")

    data = {}
    for row in rows:
        TDs = row.find_all(name="td")
        
        year, month, day = TDs[0].text.split("/")
        year, month, day = jalali_to_gregorian(int(year), int(month), int(day))
        date = datetime.date(year, month, day)
        before = int(TDs[2].text.replace(",", ""))
        after = int(TDs[1].text.replace(",", ""))

        data[date] = {
            "before": before, 
            "after": after,
            "rate": after / before
        }

    return pd.DataFrame(data).transpose()


def status_changes(num_id: int | str) -> dict:
    page = get(__BASE_URL__ + f"Loader.aspx?Partree=15131L&i={num_id}")   
    if "Error" in page.text:
            print("Internal Server Error")
            return None
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find(name="tbody")
    rows = table.find_all(name="tr")
    data = {}
    for row in rows:
        date, time, status = row.find_all(name="td")

        year, month, day = date.text.split("/")
        year, month, day = jalali_to_gregorian(int(year), int(month), int(day))
        hour, minute, second = time.text.split(":")
        TIME = datetime.date(int(year), int(month), int(
            day), int(hour), int(minute), int(second))
        data[TIME] = status.text
    return data


def ID(num_id: int | str, original=False) -> dict:
    page = get(__BASE_URL__ + f"Loader.aspx?Partree=15131M&i={num_id}")   
    if "Error" in page.text:
            print("Internal Server Error")
            return None
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find(name="tbody")
    rows = table.find_all(name="tr")
    data = {}
    for row in rows:
        td = row.find_all(name="td")
        data[td[0].text] = td[1].text

    if original:
        return data
    else:
        return {
            "symbol_12digit_code": data["کد 12 رقمی نماد"],
            "symbol_5digit_code": data["کد 5 رقمی نماد"],
            "latin": data["نام لاتین شرکت"],
            "company_4digit_code": data["کد 4 رقمی شرکت"],
            "company_name": data["نام شرکت"],
            "persian_symbol": data["نماد فارسی"],
            "persian_30digit_symbol": data["نماد 30 رقمی فارسی"],
            "company_12digit_code": data["کد 12 رقمی شرکت"],
            "market": data["بازار"],
            "table_code": data["کد تابلو"],
            "group_code": data["کد گروه صنعت"],
            "group": data["گروه صنعت"],
            "subgroup_code": data["کد زیر گروه صنعت"],
            "subgroup": data["زیر گروه صنعت"]
        }


def codal_top_new():
    r = get("http://www.tsetmc.com/tsev2/data/CodalTopNew.aspx")
    t = r.text

    values = []
    start = 0

    bracets = -1

    for i in range(len(t)):
        if t[i] == "[":
            if bracets == 0:
                start = i
            #print("[   ", bracets, end="  ->  ")
            bracets += 1
            # print(bracets)
        elif t[i] == "]":
            #print("]   ", bracets, end="  ->  ")
            bracets -= 1
            # print(bracets)
            if bracets == 0:
                end = i
                values.append(t[start+1: end])

    len(values)
    for v in values:
        Vs = v.split(",")
        for i in Vs:
            print(i)

        print("\n", 25*"-", "\n")

        # - - - - - - - - - - - - - - - TO DO - - - - - - - - - - - - - - - - - - - - - - - -


def all_tickers(original=False, stock=True, stock_rights=True, other=False) -> pd.DataFrame:
    page = get("http://www.tsetmc.com/Loader.aspx?ParTree=111C1417")   
    if "Error" in page.text:
            print("Internal Server Error")
            return None
        
    soup = BeautifulSoup(page.content, "html.parser")
    rows = soup.find(name="table").find_all(name="tr")

    DATA = {}

    for row in rows[1:]:
        values = [td.text for td in row.find_all(name="td")]
        num_id = row.find_all("td")[6].find(
            name="a").get_attribute_list("href")[0].split("=")[-1]
        DATA[num_id] = values

    
    df = pd.DataFrame(DATA).transpose()
    df.columns = ["symbol_code", "sector", "industry_group", "type", "en_symbol", "en_name", "symbol", "name"]
    
    if not stock:
        df = df[~ df.symbol_code.str.startswith("IRO")]
    if not stock_rights:
        df = df[~ df.symbol_code.str.startswith("IRR")]
    if not other:
        df = df[df.symbol_code.str.startswith("IRR") | df.symbol_code.str.startswith("IRO")]
    
    if original:
        df.columns = [td.text for td in rows[0].find_all(name="td")]      
    return df


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
