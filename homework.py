import datetime as dt


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        """Add new record."""
        self.records.append(record)

    def get_today_stats(self):
        """Count records for today."""
        today = dt.date.today()
        return sum(record.amount for record in self.records
                   if record.date == today)

    def get_week_stats(self):
        """Count records for one week."""
        today = dt.date.today()
        week = dt.timedelta(days=6)
        return sum(record.amount for record in self.records
                   if today - week <= record.date <= today)

    def today_count(self):
        """Limit calculation."""
        day_counter = self.limit - self.get_today_stats()
        return day_counter


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        """Counting calories in different currencies."""
        today_count = self.today_count()
        if today_count > 0:
            return ('Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {today_count} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    EURO_RATE = 91.85
    USD_RATE = 75.69
    RUB_RATE = 1.0

    def get_today_cash_remained(self, currency):
        """Counting money in different currencies."""
        today_count = self.today_count()
        if today_count == 0:
            return 'Денег нет, держись'
        course = {
            'rub': (CashCalculator.RUB_RATE, 'руб'),
            'usd': (CashCalculator.USD_RATE, 'USD'),
            'eur': (CashCalculator.EURO_RATE, 'Euro')
        }
        rate, valuta = course[currency]
        balance = round(today_count / rate, 2)
        if currency not in course:
            raise ValueError('Неподдерживаемая валюта')
        if balance > 0:
            return f'На сегодня осталось {balance} {valuta}'
        balance = abs(balance)
        return f'Денег нет, держись: твой долг - {balance} {valuta}'
