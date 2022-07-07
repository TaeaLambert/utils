from dateutil.relativedelta import relativedelta
from datetime import datetime


def relative_date(years: int = 0, months: int = 0, day: int = 0) -> datetime:
    return datetime.today().replace(
        hour=0, minute=0, second=0, microsecond=0
    ) + relativedelta(years=years, months=months, days=day)
