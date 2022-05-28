from ...tools import get, jalali_to_gregorian, td_to_int
from bs4 import BeautifulSoup
import datetime
import pandas as pd

BASE_URL = "http://www.tsetmc.com/Loader.aspx"

Partree = {
    "watcher_messages": "151313",
    "most_traded": "151317",
    "share_change": "151310",
    "market_cap_change": "15131A",
    "value": "15131B",
    "volume": "15131C"   
}

def watcher_messages(Flow:int=0):
    """
    0 : عمومي - مشترک بين بورس و فرابورس
    1 : بورس
    2 : فرابورس
    3 : آتی
    4 : پایه فرابورس
    5 : پایه فرابورس (منتشر نمی شود)
    6 : بورس انرژی
    7 : بورس کالا
    """
    page = get(BASE_URL, params = {"Partree":"151313", "Flow":Flow})
    soup = BeautifulSoup(page.content, "html.parser")

    rows = soup.find(name="tbody").find_all(name="tr")

    DATA = {}
    for i in range(0, len(rows), 2):
        title = rows[i].find_all(name="th")[0].text
        DT = rows[i].find_all(name="th")[1].text
        date, time = DT.split(" ")
        year, month, day = date.split("/")
        year, month, day = jalali_to_gregorian(int(year) + 1400, int(month), int(day))
        hour, minute = time.split(":")
        DT = datetime.datetime(year, month, day, int(hour), int(minute))
        message = rows[i+1].find(name="td").text
        DATA[DT] = {
            "title": title,
            "message": message
        }
        
    return pd.DataFrame(DATA).transpose()

def most_traded(Flow:int=1):
    """
    1 : بورس
    2 : فرابورس
    """
    page = get(BASE_URL, params = {"Partree":"151317","Type":"MostVisited", "Flow":Flow})
    soup = BeautifulSoup(page.content, "html.parser")

    rows = soup.find(name="tbody").find_all(name="tr")
    
    DATA = {}
    for row in rows:
        TDs = row.find_all(name="td")
        
        num_id = TDs[0].find(name="a").get_attribute_list("href")[0].split("=")[-1]
        
        DATA[num_id] = {
            "symbol": TDs[0].text,
            "name": TDs[1].text,
            "yesterday": td_to_int(TDs[2]),
            "close":  td_to_int(TDs[3]),
            "last": td_to_int(TDs[6]),
            "low": td_to_int(TDs[9]),
            "high": td_to_int(TDs[10]),
            "count": td_to_int(TDs[11]),
            "volume": td_to_int(TDs[12]),
            "value": td_to_int(TDs[13])
        }
    return pd.DataFrame(DATA).transpose()

def share_changes(Flow:int=1):
    """
    1 : بورس
    2 : فرابورس
    """
    page = get(BASE_URL, params = {"Partree":"151310","Flow":Flow})
    soup = BeautifulSoup(page.content, "html.parser")

    rows = soup.find(name="tbody").find_all(name="tr")
    
    DATA = []
    for row in rows:
        TDs = row.find_all(name="td")
        
        DATA.append(
            {
                "num_id": TDs[0].find(name="a").get_attribute_list("href")[0].split("=")[-1],
                "symbol": TDs[0].text,
                "name": TDs[1].text,
                "date": TDs[2].text,
                "new": td_to_int(TDs[3]),
                "old": td_to_int(TDs[4])
            }
        )
    
    return pd.DataFrame(DATA)

def market_cap_changes(Flow:int=1):
    """
    1 : بورس
    2 : فرابورس
    """
    page = get(BASE_URL, params = {"Partree":"15131A", "Flow":Flow})
    soup = BeautifulSoup(page.content, "html.parser")
    
    def extract(i):   
        table = soup.find_all(name="tbody")[i].find_all(name="tr")
        data = {}
        for row in table:
            TDs = row.find_all(name="td")
            
            num_id = TDs[0].find(name="a").get_attribute_list("href")[0].split("=")[-1],
                
            data[num_id] = {
                "symbol": TDs[0].text,
                "name": TDs[1].text,
                "value": td_to_int(TDs[2]),
                "change": td_to_int(TDs[3])
                }
        return pd.DataFrame(data).transpose()
            
    return {
        "increases": extract(0),
        "decreases": extract(1)
    }
    
def top_trading(Flow:int=1, by:str="volume"):
    """
    0 : عمومي - مشترک بين بورس و فرابورس
    1 : بورس
    2 : فرابورس
    3 : آتی
    4 : پایه فرابورس
    5 : پایه فرابورس (منتشر نمی شود)
    6 : بورس انرژی
    7 : بورس کالا
    """
    if by not in ["volume", "value"]:
        return
    
    page = get(BASE_URL, params = {"Partree":Partree[by], "Flow":Flow})
    soup = BeautifulSoup(page.content, "html.parser")

    rows = soup.find(name="tbody").find_all(name="tr")

    DATA = {}
    for row in rows:
        TDs = row.find_all(name="td")
        num_id = TDs[0].find(name="a").get_attribute_list("href")[0].split("=")[-1]
        
        DATA[num_id] = {
            "symbol": TDs[0].text,
            "name": TDs[1].text,
            "count": td_to_int(TDs[2]),
            "volume": td_to_int(TDs[3]),
            "value": td_to_int(TDs[4]),
            "marketcap": td_to_int(TDs[5])
            }
    return pd.DataFrame(DATA).transpose()

def best_asks_and_bids(Flow:int=1):
    page = get(BASE_URL, params = {"Partree":"151318", "Flow":Flow})
    soup = BeautifulSoup(page.content, "html.parser")

    def extract(i):
        rows = soup.find_all(name="tbody")[i].find_all(name="tr")
        DATA = []
        for row in rows:
            TDs = row.find_all(name="td")
            num_id = TDs[0].find(name="a").get_attribute_list("href")[0].split("=")[-1]
        
            DATA.append(
                {
                    "num_id": num_id,
                    "price": td_to_int(TDs[1]),
                    "volume": td_to_int(TDs[2]),
                    "value": td_to_int(TDs[3]),
                    "count": td_to_int(TDs[4])
                }
            )
        return pd.DataFrame(DATA)
    return {
        "asks": extract(0),
        "bids": extract(1)
    }
    
def best_industry_groups():
    page = get(BASE_URL, params = {"Partree":"15131O"})
    soup = BeautifulSoup(page.content, "html.parser")
    rows = soup.find(name="tbody").find_all(name="tr")
    
    DATA = {}
    for row in rows:
        TDs = row.find_all(name="td")
        name = TDs[0].text
        DATA[name] = {
            "market_cap": td_to_int(TDs[1]),
            "trades_count": td_to_int(TDs[2]),
            "trades_volume": td_to_int(TDs[3]),
            "trades_value": td_to_int(TDs[4])
        }
        
    return pd.DataFrame(DATA).transpose()

def market_cap_history(Flow:int=1):
    page = get(BASE_URL, params = {"Partree":"15131N", "Flow":Flow})
    soup = BeautifulSoup(page.content, "html.parser")
    rows = soup.find(name="tbody").find_all(name="tr")
    
    DATA = {}
    for row in rows:
        TDs = row.find_all(name="td")
        year, month, day = TDs[0].text.split("/")
        
        year = int(year)
        if year < 30:
            year += 1400
        else:
            year += 1300
            
        year, month, day = jalali_to_gregorian(year, int(month), int(day))
        date = datetime.date(year, month, day)
        DATA[date] = td_to_int(TDs[1])
    return pd.Series(DATA)
