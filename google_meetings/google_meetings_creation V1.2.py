import os
from datetime import datetime
from typing import Literal
from flask import redirect
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build, Resource
from google.oauth2 import service_account

# https://www.youtube.com/watch?v=_uHd0ypR5OI
# https://www.youtube.com/watch?v=1JkKtGFnua8
# https://developers.google.com/calendar/api/v3/reference/events/insert
# https://developers.google.com/resources/api-libraries/documentation/calendar/v3/python/latest/calendar_v3.events.html#insert

# TODO: Talk to benoit about service account vs api key for this microapp


def google_crential_env_to_file():
    with open(os.getenv("GOOGLE_CONFIG_LOCATION"), "w") as f:
        f.write(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))


def get_gmt(country: str) -> str:
    return "-12:00"


class Google_calendar_api_error(Exception):
    """This exception is raised when Hubspot return a non 200 status code"""

    def __init__(self, issue: str, status_code: int):
        self.issue = issue
        self.status_code = status_code

    def __str__(self):
        return f"Google api error: {self.issue} returned a {self.status_code} status code"


class google_meeting:
    def __init__(self, response: dict, *args, **kwargs):
        self.start_time = response.get("start").get("dateTime")
        self.end_time = response.get("end").get("dateTime")
        self.summary = response.get("summary")
        self.url = response.get("htmlLink")
        self.data = response

    @property
    def redirect(self):
        return redirect(self.url)


class calendar_events_service_account:
    def __init__(self, api_name: str, api_version: str, cred_location: str):
        if not os.path.exists(cred_location):
            google_crential_env_to_file()
        creds = service_account.Credentials.from_service_account_file(cred_location)
        service: Resource = build(api_name, api_version, credentials=creds)
        self.service = service.events()

    def create_meeting(self, calendar_id: str, start_time: datetime, end_time: datetime, *args, **kwargs) -> google_meeting:

        # PDT/MST/GMT-12
        GMT_OFF = "-12:00" if "country" not in kwargs else get_gmt(kwargs["country"])
        # TODO pycountry get gmt offset from country passed in otherwise get New Zealand GMT offset.

        send_updates = None if "send_updates" not in kwargs else kwargs["send_updates"]
        supports_attachments = False if "supports_attachments" not in kwargs else kwargs["supports_attachments"]
        max_attendees = 10 if "max_attendees" not in kwargs else kwargs["max_attendees"]
        visibility = "public" if "visibility" not in kwargs else kwargs["visibility"]

        request = self.service.insert(
            calendarId=calendar_id,
            body={
                "start": {"dateTime": "2022-09-08T12:00:00-12:00"},
                "end": {"dateTime": "2022-09-08T14:00:00-12:00"},
                "summary": "Dinner with friends",
                "visability": visibility,
                "anyoneCanAddSelf": True,
            },
            maxAttendees=max_attendees,
            supportsAttachments=supports_attachments,
            sendUpdates=send_updates if send_updates != None else "none",
        )

        try:
            response = request.execute()
            print(response)
        except HttpError as error:
            raise Google_calendar_api_error(error.reason, error.status_code)
        except Exception as e:
            raise e

        return google_meeting(response)


def start():
    calendar_id = os.getenv("calendar_id")
    supports_attachments: bool = False
    send_updates: Literal("all", "externalOnly", "none") = "none"
    max_attendees: int = 10
    visibility: Literal("default", "public", "private", "confidential") = "public"

    service = calendar_events_service_account("calendar", "v3", os.getenv("GOOGLE_CONFIG_LOCATION"))
    try:
        response = service.create_meeting(
            calendar_id,
            datetime.now(),
            datetime.now(),
            supports_attachments=supports_attachments,
            send_updates=send_updates,
            max_attendees=max_attendees,
            visibility=visibility,
            conferenceDataVersion=1,
        )
    except Google_calendar_api_error as error:
        print("Google_calendar_error")
        return error
    except Exception as e:
        print("This is a error that has no exception.")
        return e

    return response

    # https://calendar.google.com/calendar/u/0/r/eventedit
    # ?text=An+amazing+event+%F0%9F%A5%B3
    # &dates=20220622T150000/20220622T170000
    # &ctz=America/Los_Angeles
    # &details=This+is+an+event+description.+Add+information+about+your+event+here!+%F0%9F%91%8B%0A%0ALorem+ipsum+dolor+sit+amet,+consectetur+adipiscing+elit.+Sed+tempor+vehicula+metus,+ac+rutrum+nulla+finibus+et.+Nunc+egestas+pellentesque+quam+in+feugiat.+Aenean+scelerisque+lacus+sed+eros+aliquet+dignissim.+Aliquam+erat+volutpat.+Etiam+a+metus+interdum,+egestas+est+sed,+gravida+nisl.+Duis+fringilla+est+sed+arcu+tincidunt+semper.+Morbi+rutrum+nisl+nunc,+quis+tempus+dui+pharetra+tristique.+Vestibulum+a+dolor+sit+amet+nunc+venenatis+convallis+non+tempus+lorem.
    # &location=https://zoom.us/meeting-link
    # &pli=1
    # &uid=1662512534addeventcom
    # &sf=true
    # &output=xml


#


print(start())
