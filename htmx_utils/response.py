from typing import Self
from django.http import HttpResponse

from htmx_utils.constants import ResponseHeaders, Swap, TriggerType


class HtmxResponse(HttpResponse):
    def trigger(
        self,
        trigger: str | dict[str, str] | list[str],
        type: TriggerType = TriggerType.DEFAULT,
    ) -> Self:
        self.headers[type.value] = trigger  # type: ignore
        return self

    def reswap(self, type: Swap) -> Self:
        self.headers[ResponseHeaders.RESWAP.value] = type.value  # type: ignore
        return self

    def retarget(self, target: str):
        self.headers[ResponseHeaders.RETARGET.value] = target  # type: ignore
        return self
