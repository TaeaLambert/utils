class IntegrationGlueException(Exception):
    pass


class HubspotAPIError(IntegrationGlueException):
    """This exception is raised when Hubspot return a non 200 status code"""

    def __init__(self, issue: str, status_code: int):
        self.issue = issue
        self.status_code = status_code

    def __str__(self):
        return f"Hubspot API error {self.issue} returned a {self.status_code} status code"

    def to_string(self):
        return str(self.__str__())


class HubspotAPIServerError(IntegrationGlueException):
    """This exception is raised when Hubspot return a non 200 status code"""

    def __init__(self, issue: str, status_code: int, text: str):
        self.issue = issue
        self.status_code = status_code
        self.text = text

    def __str__(self):
        return f"Hubspot Server Error {self.issue} returned a {self.status_code} status code"

    def to_string(self):
        return str(self.__str__())


class HubspotAPILimitReached(HubspotAPIError):
    def __init__(self, issue: str, status_code: int):
        self.issue = issue
        self.status_code = status_code

    def __str__(self):
        return f"Hubspot API limmit reached. {self.issue} returned a {self.status_code} status code"

    def to_string(self):
        return str(self.__str__())
