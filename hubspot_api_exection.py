class IntegrationGlueException(Exception):
    pass


class HubspotAPIError(IntegrationGlueException):
    """This exception is raised when Hubspot return a non 200 status code"""

    def __init__(self, issue: str, status_code: int):
        self.issue = issue
        self.status_code = status_code

    def __str__(self):
        return (
            f"Hubspot API error {self.issue} returned a {self.status_code} status code"
        )

    def to_string(self):
        return str(self.__str__())


class HubspotAPILimitReached(HubspotAPIError):
    def __str__(self):
        return f"Hubspot API error {self.issue} API LIMIT REACHED"
