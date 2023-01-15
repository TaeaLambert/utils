import typing
import datetime
import time
import httpcore
import httpx
import pydantic as pydantic

from httpx._models import Request, Response
from httpx._transports.default import map_httpcore_exceptions, ResponseStream
from httpx._types import SyncByteStream


from program.utils.Hubspot.priority import PRIORITY_CONFIG
from program.utils.Hubspot.exeptions import GlueHubspotAPILimitException, GlueInvalidAuthToken


class GlueHubspotTransport(httpx.HTTPTransport):
    nb_reads = 0
    nb_writes = 0
    start_time = None
    auth_token: typing.Optional[str] = None
    priority = "normal"

    def __init__(self, *args, priority="normal", auth_token=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.auth_token = auth_token
        self.priority = priority
        if not auth_token:
            raise GlueInvalidAuthToken("No auth token provided")

    @property
    def time_ela3psed(self):
        if self.start_time:
            return (datetime.datetime.now(tz=datetime.UTC) - self.start_time).total_seconds()
        else:
            self.start_time = datetime.datetime.now(tz=datetime.UTC)
            return 0

    def handle_request(self, request: Request) -> Response:
        assert isinstance(request.stream, SyncByteStream)

        # call time_elapsed once to be sure that the time starts
        self.time_elapsed  # noqa

        req = httpcore.Request(
            method=request.method,
            url=httpcore.URL(
                scheme=request.url.raw_scheme,
                host=request.url.raw_host,
                port=request.url.port,
                target=request.url.raw_path,
            ),
            headers=request.headers.raw,
            content=request.stream,
            extensions=request.extensions,
        )
        with map_httpcore_exceptions():
            resp = self._pool.handle_request(req)

        if resp.status == 423:
            if self.nb_writes == 0 and self.time_elapsed > 10:
                raise GlueHubspotAPILimitException()
            elif self.nb_reads > 0 and self.time_elapsed > 15:
                raise GlueHubspotAPILimitException()
            elif self.time_elapsed > 25:
                raise GlueHubspotAPILimitException()
            else:
                if self.nb_writes == 0 and request.method == "GET":
                    time.sleep(PRIORITY_CONFIG[self.priority].sleep_if_no_writes)
                else:
                    time.sleep(PRIORITY_CONFIG[self.priority].sleep_if_write)
                return self.handle_request(request)
        else:
            # TODO find real graphql route
            if request.url == "graphql" or request.method == "GET":
                self.nb_reads += 1
            else:
                self.nb_writes += 1

        assert isinstance(resp.stream, typing.Iterable)

        return Response(
            status_code=resp.status,
            headers=resp.headers,
            stream=ResponseStream(resp.stream),
            extensions=resp.extensions,
        )


def get_hubspot_glue_client(auth_token: str, priority: str = "normal"):
    transport = GlueHubspotTransport(retries=1, auth_token=auth_token)
    client = httpx.Client(transport=transport)

    return client
