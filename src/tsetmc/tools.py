import datetime
import requests

def get(url, params=None):
    response = requests.get(
        url,
        params=params,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    )
    if response.status_code != 200:
        response.raise_for_status()
    else:
        return response

def td_to_int(td):        
    try: result = td.find(name="div").get_attribute_list("title")[0]
    except: result = td.text
    finally: result = int(result.replace(",", ""))
    return result

def search(search_key:str) -> dict:
    """gets a ticker name or symbol and returns its num_id"""
    
    response = get(f'http://www.tsetmc.com/tsev2/data/search.aspx?skey={search_key}')
    # best match :
    result = response.text.split(";")[0]

    if not result:
        return None

    symbol, name, num_id = result.split(",")[:3]
    return {
        "symbol": symbol,
        "name": name,
        "num_id": int(num_id)
    }

def hEven_to_time(time: str|int) -> datetime.time:
    time = str(time)
    hour, minute, second = time[:-4], time[-4:-2], time[-2:]
    return datetime.time(int(hour), int(minute), int(second))

def time_to_hEven(time: datetime.time, seperated=False) -> tuple|str:
    hour = str(time.hour)
    if time.minute < 10 :
        minute = "0" + str(time.minute)
    else:
        minute = str(time.minute)
    if time.second < 10 :
        second = "0" + str(time.second)
    else:
        second = str(time.second)
        
    if seperated:
        return hour, minute, second
    else:
        return hour + minute + second
    
def dEven_to_date(date: str|int) -> datetime.date:
    date = str(date)
    year, month, day = date[:-4], date[-4:-2], date[-2:]
    return datetime.date(int(year), int(month), int(day))

def date_to_dEven(date: datetime.date, seperated=False) -> tuple|str:
    year = str(date.year)
    if date.month < 10 :
        month = "0" + str(date.month)
    else:
        month = str(date.month)
    if date.day < 10 :
        day = "0" + str(date.day)
    else:
        day = str(date.day)
        
    if seperated:
        return year, month, day
    else:
        return year + month + day


def jalali_to_gregorian(jy, jm, jd):
    jy += 1595
    days = -355668 + (365 * jy) + ((jy // 33) * 8) + (((jy % 33) + 3) // 4) + jd
    if (jm < 7):
        days += (jm - 1) * 31
    else:
        days += ((jm - 7) * 30) + 186
    gy = 400 * (days // 146097)
    days %= 146097
    if (days > 36524):
        days -= 1
        gy += 100 * (days // 36524)
        days %= 36524
        if (days >= 365):
            days += 1
    gy += 4 * (days // 1461)
    days %= 1461
    if (days > 365):
        gy += ((days - 1) // 365)
        days = (days - 1) % 365
    gd = days + 1
    if ((gy % 4 == 0 and gy % 100 != 0) or (gy % 400 == 0)):
        kab = 29
    else:
        kab = 28
    sal_a = [0, 31, kab, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    gm = 0
    while (gm < 13 and gd > sal_a[gm]):
        gd -= sal_a[gm]
        gm += 1
    return [gy, gm, gd]

def gregorian_to_jalali(gy, gm, gd):
    g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    if (gm > 2):
        gy2 = gy + 1
    else:
        gy2 = gy
    days = 355666 + (365 * gy) + ((gy2 + 3) // 4) - ((gy2 + 99) //
                                                        100) + ((gy2 + 399) // 400) + gd + g_d_m[gm - 1]
    jy = -1595 + (33 * (days // 12053))
    days %= 12053
    jy += 4 * (days // 1461)
    days %= 1461
    if (days > 365):
        jy += (days - 1) // 365
        days = (days - 1) % 365
    if (days < 186):
        jm = 1 + (days // 31)
        jd = 1 + (days % 31)
    else:
        jm = 7 + ((days - 186) // 30)
        jd = 1 + ((days - 186) % 30)
    return [jy, jm, jd]