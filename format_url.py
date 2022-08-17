from requests.utils import quote as urlquote


def format_url(url: str) -> str:
    """_summary_

    Args:
        url (str): This is a url that has not been formatted.

    Returns:
        str: Returns a formatted url. (replace " " with "-" --> .lower() --> utf-8 encoded)
    """
    formatted_url = url.replace(" ", "-").lower()
    try:
        formatted_url_done = urlquote(formatted_url)
    except Exception as e:
        return e
    # encode formatted_url to utf-8
    return formatted_url_done
