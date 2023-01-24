from fastapi import Header, Request
from pydantic import BaseModel
from typing import Dict, Union


class HubspotRequest(BaseModel):
    pass


class WorkflowRequest(Request):
    callbackId: str
    origin: Dict
    context: Dict
    object: Dict
    fields: Dict = None
    inputFields: Dict = None


class HubspotAppLogin(HubspotRequest):
    code: str = None
