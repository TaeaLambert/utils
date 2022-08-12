import json
from utils.date import relative_date


def get_wrike_queary_dates(ahead: int = 6, past: int = 13) -> str:
    """
    This function takes the number of months ahead and the number of months past
    Both arguments are positive integers and default to 6 and 13 respectively
    """
    print("Getting Wrike query dates...")
    print("Ahead:", ahead)
    print("Past:", past)
    six_month_ahead = relative_date(months=ahead)
    thirteen_month_behind = relative_date(months=-past)

    print(six_month_ahead)
    print(thirteen_month_behind)
    return json.dumps(
        {
            "start": thirteen_month_behind.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "end": six_month_ahead.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
    )
