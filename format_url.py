from requests.utils import quote as urlquote


def format_url(url: str) -> str:
    """_summary_

    Args:
        url (str): This is a url that has not been formatted.

    Returns:
        str: Returns a formatted url. (replace " " with "-" --> .lower() --> utf-8 encoded)
    """
    formatted_url = url.replace(" ", "-").lower()
    # encode formatted_url to utf-8
    return urlquote(formatted_url)
