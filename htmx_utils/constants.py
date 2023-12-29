from enum import Enum


class ResponseHeaders(Enum):
    LOCATION = "HX-Location"
    PUSH_URL = "HX-Push-Url"
    REDIRECT = "HX-Redirect"
    REFRESH = "HX-Refresh"
    REPLACE_URL = "HX-Replace-Url"
    RESWAP = "HX-Reswap"
    RETARGET = "HX-Retarget"
    RESELECT = "HX-Reselect"
    TRIGGER = "HX-Trigger"
    TRIGGER_AFTER_SETTLE = "HX-Trigger-After-Settle"
    TRIGGER_AFTER_SWAP = "HX-Trigger-After-Swap"


class TriggerType(Enum):
    DEFAULT = "HX-Trigger"
    AFTER_SETTLE = "HX-Trigger-After-Settle"
    AFTER_SWAP = "HX-Trigger-After-Swap"


class Swap(Enum):
    INNER = "innerHTML"
    OUTER = "outerHTML"
    BEFOREBEGIN = "beforebegin"
    AFTERBEGIN = "afterbegin"
    BEFOREEND = "beforeend"
    AFTEREND = "afterend"
    DELETE = "delete"
    NONE = "none"
