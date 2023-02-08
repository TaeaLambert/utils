from typing import Literal
from pydantic import BaseModel


class Origin(BaseModel):
    """example

      "origin": {
      "portalId": 22412849,
      "actionDefinitionId": 27216707,
      "actionDefinitionVersion": 1,
      "extensionDefinitionId": 27216707,
      "extensionDefinitionVersionId": 1
    }
    """

    portalId: str or int = None
    actionDefinitionId: str or int = None
    actionDefinitionVersion: str or int = None
    extensionDefinitionId: str or int = None
    extensionDefinitionVersionId: str or int = None


class Context(BaseModel):
    """Example:
    "context": {
      "source": "WORKFLOWS",
      "workflowId": 319544947
    }
    """

    source: Literal["WORKFLOWS"]
    workflowId: int or None = None


class Object(BaseModel):
    """Example:
     "object": {
      "objectId": 7002,
      "objectType": "CONTACT"
    }
    """

    objectId: str or int
    objectType: str


class BaseWorkflowRequest(BaseModel):
    """example
    {
    "callbackId": "ap-22412849-465078523931-2-0",
    "origin": {
        "portalId": 22412849,
        "actionDefinitionId": 27216707,
        "actionDefinitionVersion": 3,
        "extensionDefinitionId": 27216707,
        "extensionDefinitionVersionId": 3
    },
    "context": {
        "source": "WORKFLOWS",
        "workflowId": 319544947
    },
    "object": {
        "objectId": 7002,
        "objectType": "CONTACT"
    },
    "fields": {
        "From property": "Contact:firstname",
        "To property": "Contact:firstname",
        "Format Type": "Caps"
    },
    "inputFields": {
        "From property": "Contact:firstname",
        "To property": "Contact:firstname",
        "Format Type": "Caps"
    }
    }
    """

    callbackId: str
    origin: Origin
    context: Context
    object: Object


class BaseDropdownRequest(BaseModel):
    """Example:
    {
      "origin": {
        "portalId": 22412849,
        "actionDefinitionId": 27216707,
        "actionDefinitionVersion": 1,
        "extensionDefinitionId": 27216707,
        "extensionDefinitionVersionId": 1
      },
      "inputFieldName": "Format Type",
      "fetchOptions": {},
      "fields": {
        "Format Type": {
          "fieldKey": "Format Type",
          "fieldValue": {
            "valueType": "EXTERNAL",
            "value": "Caps",
            "effectiveValueType": "SINGLE"
          }
        },
        "From property": {
          "fieldKey": "From property",
          "fieldValue": {
            "valueType": "EXTERNAL",
            "value": "Contact:firstname",
            "effectiveValueType": "SINGLE"
          }
        },
        "To property": {
          "fieldKey": "To property",
          "fieldValue": {
            "valueType": "EXTERNAL",
            "value": "Contact:firstname",
            "effectiveValueType": "SINGLE"
          }
        }
      },
      "portalId": 22412849,
      "extensionDefinitionId": 27216707,
      "extensionsDefinitionVersion": 1,
      "inputFields": {
        "Format Type": {
          "type": "STATIC_VALUE",
          "value": "Caps"
        },
        "From property": {
          "type": "STATIC_VALUE",
          "value": "Contact:firstname"
        },
        "To property": {
          "type": "STATIC_VALUE",
          "value": "Contact:firstname"
        }
      }
    }"""

    origin: Origin = None
    portalId: str or int = None
    extensionDefinitionId: str or int = None
    extensionDefinitionVersionId: str or int = None
    fetchOptions: dict
    inputFieldName: str
    pass


class WorkflowRequest(BaseWorkflowRequest):
    fields: dict = None
    inputFields: dict = None


class DropdownRequest(BaseDropdownRequest):
    fields: dict = None
    inputFields: dict = None
