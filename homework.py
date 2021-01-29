import datetime as dt


class Record:
    def __init__(self, amount, comment, date = None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


    def show(self):
        """formatted data output"""
        return self.amount, self.comment, self.date


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []


    def add_record(self, record):
        """add new record"""
        self.records.append(record)


    def get_today_stats(self):
        """count records for today"""
        today = dt.date.today()
        return sum(record.amount
                for record in self.records
                if record.date == today)


    def get_week_stats(self):
        """count records for one week"""
        today = dt.date.today()
        week = dt.timedelta(days = 6)
        return sum(record.amount
                for record in self.records
                if today - week <= record.date <= today)


    def today_count(self):
        """limit calculation"""
        day_counter = self.limit - self.get_today_stats()
        return day_counter


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        """counting calories"""
        today_count = self.today_count()
        if today_count > 0:
            return ('Сегодня можно съесть что-нибудь ещё,'
                    f'но с общей калорийностью не более {today_count} кКал')
        return f'Хватит есть!'


class CashCalculator(Calculator):
    EURO_RATE = 91.85
    USD_RATE = 75.69


    def get_today_cash_remained(self, currency):
        """counting money in different currencies"""
        course = {
            'rub': (1, 'руб'),
            'usd': (CashCalculator.USD_RATE, 'USD'),
            'eur': (CashCalculator.EURO_RATE, 'Euro')
     }
        if currency not in course:
            return 'Неподдерживаемая валюта'
        today_count = self.today_count()
        if today_count == 0:
            return f'Денег нет, держись'
        rate, valuta = course[currency]
        balance = round(today_count / rate, 2)
        if balance > 0:
            return f'На сегодня осталось {balance} {valuta}'
        balance = abs(balance)
        return f'Денег нет, держись: твой долг - {balance} {valuta}'
