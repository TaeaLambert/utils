import re


def format_url(url: str) -> str:
    """_summary_

    Args:
        url (str): This is a url that has not been formatted.

    Returns:
        str: Returns a formatted url. (replace " " with "-" --> .lower() --> replace all special char beside '-')
    """
    formatted_url = url.replace(" ", "-").lower()
    # try:
    #     formatted_url_done = urlquote(formatted_url)
    # except Exception as e:
    #     return e

    # This is a change as url encocder changes a ! to %21 and hubspot dies if a % is passed into the url and returns a error for a #
    formatted_url_done = re.sub("[^A-Za-z0-9 -]+", "", formatted_url)

    # encode formatted_url to utf-8
    return formatted_url_done
