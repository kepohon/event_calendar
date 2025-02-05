''' ymd.py '''

import datetime

class YMD:
    _year = 0
    _month = 0
    _day = 0
    
    def __init__(self):
        self._year = datetime.date.today().year
        self._month = datetime.date.today().month
        self._day = datetime.date.today().day
    
    # Getter
    @property
    def year(self):
        return self._year
    
    @property
    def month(self):
        return self._month
    
    @property
    def day(self):
        return self._day
    
    # Setter
    @year.setter
    def year(self, value):
        if value >= 0 and value < 10000:
            self._year = value
        else:
            print("year number error!")
    
    @month.setter
    def month(self, value):
        if value >= 1 and value <= 12:
            self._month = value
        else:
            print("month number error!")
    
    @day.setter
    def day(self, value):
        if value >= 1 and value <= 31:
            self._day = value
        else:
            print("day number error!")
    



if __name__ == '__main__':
    ymd = YMD()
    print(f"{ymd.year}/{ymd.month}/{ymd.day}")
