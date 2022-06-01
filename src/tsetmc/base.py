from . import Get
from .tools import search
from .Get import today


class Ticker:
    def __init__(self, symbol=None, name=None, num_id=None):
        self.num_id = num_id

        search_key = symbol or name
        
        if search_key != None:
            data = search(search_key)
            if not data:
                return None
            self.symbol = data["symbol"]
            self.name = data["name"]
            self.num_id = data["num_id"]
        
        if self.num_id != None:
            data = Get.basics(self.num_id)
            self.symbol = data["LVal18AFC"]
            self.section_name = data["LSecVal"]
            self.symbol_group_code = data["CgrValCot"]
            self.market = data["Flow"] 
            """
            0 : عمومي - مشترک بين بورس و فرابورس
            1 : بورس
            2 : فرابورس
            3 : آتی
            4 : پایه فرابورس
            5 : پایه فرابورس (منتشر نمی شود)
            """
            self.instrument_id = data["InstrumentID"]
            self.instrument_code = data["InsCode"]
            self.base_volume = data["BaseVol"]
            self.estimated_EPS = data["EstimatedEPS"]
            self.shares_count = data["ZTitad"]
            self.company_code = data["CIsin"]
            self.sector_code = data["CSecVal"]
            self.adjusted_price = data["PClosing"]
            self.min_allowed = data["PSGelStaMax"]
            self.max_allowed = data["PSGelStaMin"]
            self.title = data["Title"]
            self.min_week = data["MinWeek"]
            self.max_week = data["MaxWeek"]
            self.min_year = data["MinYear"]
            self.max_year = data["MaxYear"]
            self.month_volume_average = data["QTotTran5JAvg"]
            self.sector_PE = data["SectorPE"]
            self.index_effect_ratio = data["KAjCapValCpsIdx"]
            self.NAV = data["NAV"]
            self.PSR = data["PSR"]

            
            data = today.general(num_id)
            if(data != None):
                self.last = data["last"]
                self.close = data["close"]
                self.first = data["first"]
                self.yesterday = data["yesterday"]
                self.low = data["low"]
                self.high = data["high"]
                self.trade_count = data["trade_count"]
                self.volume = data["volume"]
                self.value = data["value"]
                self.asks = data["asks"]
                self.bids = data["bids"]
            else:
                self.last = None
                self.close = None
                self.first = None
                self.yesterday = None
                self.low = None
                self.high = None
                self.trade_count = None
                self.volume = None
                self.value = None
                self.asks = None
                self.bids = None
            
        else:
            print("determine at least one of parameters")
            return None
        
    def general(self):
        return today.general(self.num_id)
    
    def candles(self):
        return today.candles(self.num_id)
    
    def trades(self):
        return today.trades(self.num_id)
    
    def real_legal(self):
        return Get.real_legal(self.num_id)
    
    def holders(self):
        return today.holders(self.num_id)
    
    def statistics(self):
        return Get.statistics(self.num_id)
    
    def trade_history(self, adjust=False):
        return Get.trade_history(self.num_id, adjust=adjust)
    
    def adjust_history(self):
        return Get.adjust_history(self.num_id)
    
    def status_changes(self):
        return Get.status_changes(self.num_id)
    
    def ID(self):
        return Get.ID(self.num_id)
        

class order:
    def __init__(self, count, volume, price):
        self.count = count
        self.volume = volume
        self.price = price

    def prettify(orders):
        count_len = max([len(order.count) for order in orders]) + 3
        volume_len = max([len(order.volume) for order in orders]) + 3
        price_len = max([len(order.price) for order in orders]) + 3

        result = ""
        for order in orders:
            count = str(order.count)
            count += (count_len - len(count)) * " "

            volume = str(order.volume)
            volume += (volume_len - len(volume)) * " "

            price = str(order.price)
            price += (price_len - len(price)) * " "

            result += f"{count} {volume} {price}\n"
