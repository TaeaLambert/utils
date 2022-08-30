from dateutil.relativedelta import relativedelta
from datetime import datetime


def relative_date(years: int = 0, months: int = 0, day: int = 0) -> datetime:
    """_summary_

    Args:
        years (int, optional): _description_. Defaults to 0.
        months (int, optional): _description_. Defaults to 0.
        day (int, optional): _description_. Defaults to 0.

    Example::

        # The datetime for this example is 22-08-2022 13:46:27.233

        relative_date(1)
        # returns -> datetime object (22-08-2023 13:46:27.233)

        relative_date(1,3,5)
        # returns -> datetime object (27-11-2023 13:46:27.233)

    Returns:
        datetime: This is a datetime object that has been added to from the passed in veriables
        (datetime object starts from when oject is created)
    """
    return datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) + relativedelta(
        years=years, months=months, days=day
    )


def reformat_date(date: str = datetime.today().strftime("%Y-%m-%d"), format: str = "%d-%m-%Y") -> str:
    """_summary_

    Args:
        date (str): string of a date object eg: 2022-08-22 (has to be yyyy-mm-dd). Defaults to datetime.today().strftime("%Y-%m-%d").
        format (str): the format that will be used to reformat this date (datetime package). Defaults to "%d-%m-%Y".

    Example::

        reformat_date("2022-08-22",%d-%m-%Y)
        # returns -> "22-08-2022"

    Returns:
        str: Date in format stated by the format as a string
    """
    if type(unformatted_date) != str:
        unformatted_date = str(unformatted_date)
    unformatted_date = datetime.strptime(date, "%Y-%m-%d")
    return unformatted_date.strftime(format)


def format_datetime(date: str = datetime.today().strftime("%Y-%m-%dT%H:%M:%S:%fZ"), format: str = "%d-%m-%Y %H:%M:%S") -> str:
    """_summary_

    Args:
        date (str): string of a date object eg: 2022-08-22 (has to be yyyy-mm-dd). Defaults to datetime.today().strftime("%Y-%m-%dT%H:%M:%S:%fZ").
        format (str): the format that will be used to reformat this date (datetime package). Defaults to "%d-%m-%Y %H:%M:%S".

    Example::

        reformat_date("22-08-2022T08:22:32:22Z",%d-%m-%YT%H:%M:%S)
        # returns -> "22-08-2022T08:22:32"

    Returns:
        str: Date in format stated by the format as a string
    """

    if type(unformatted_date) != str:
        unformatted_date = str(unformatted_date)
    unformatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S:%fZ")
    return unformatted_date.strftime(format)
