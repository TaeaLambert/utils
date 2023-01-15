import httpx
import typing
from program.utils.Hubspot.enums import BaseHSObjects
from program.utils.Hubspot.main_hubspot import GlueHubspotTransport, get_hubspot_glue_client


class HubspotClient:
    _client: httpx.Client

    def __init__(self, auth_token: str, priority: str = "normal"):
        self._client = get_hubspot_glue_client(auth_token, priority)

    def change_auth_token(self, auth_token: str):
        self._client._transport.auth_token = auth_token  # noqa

    def get_object(
        self,
        object_type: typing.Union[str, BaseHSObjects],
        object_id: typing.Union[str, int],
        properties: list[str],
        unique_property_key="hs_object_id",
    ):
        pass

    def get_stats(self):
        self._client._transport: GlueHubspotTransport  # noqa
        return self._client._transport.nb_read  # noqa
