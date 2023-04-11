from __future__ import annotations

from requests import Response
from singer_sdk.pagination import (
    BaseAPIPaginator,
    BasePageNumberPaginator,
    JSONPathPaginator,
)


class ZoomPageNumberPaginator(BasePageNumberPaginator):
    """
    Page number pagination method is being \
    [depricated](https://developers.zoom.us/docs/api/rest/pagination/#pagination-using-page-numbers).
    """

    def has_more(self, response: Response) -> bool:
        page_count = response.json().get("page_count", 0)
        page_number = response.json().get("page_number", 0)

        if page_number > 0:
            return page_number < page_count

        return False

    def get_next(self, response: Response) -> int | None:
        """Get the next page number.
        Args:
            response: API response object.
        Returns:
            The next page number.
        """
        return self._value + 1


class ZoomPaginator(BaseAPIPaginator):
    """
    Automatic pagination method handeling.
    """

    def __init__(self, jsonpath: str, *args, **kwargs) -> None:
        super().__init__(None)
        self._jsonpath = jsonpath
        self._paginator: BaseAPIPaginator = JSONPathPaginator(jsonpath)

    def _set_paginator(self, response: Response) -> None:
        response_keys = response.json().keys()

        if "next_page_token" in response_keys:
            self._paginator = JSONPathPaginator(self._jsonpath)
            return

        # legacy pagination
        if "page_number" in response_keys:
            self._paginator = ZoomPageNumberPaginator(start_value=1)
            return

        self._finished = True
        return

    def advance(self, response: Response) -> None:
        if not self._paginator:
            self._set_paginator(response)

        self._paginator.advance(response)
        self._count = self._paginator.count
        self._finished = self._paginator.finished

        if isinstance(self._paginator, ZoomPageNumberPaginator):
            self._value = {
                "page_number": self._paginator.current_value,
                "page_size": response.json().get("page_size"),
            }
            return

        self._value = self._paginator.current_value

    def get_next(self, response: Response) -> None:
        return

    def has_more(self, response: Response) -> bool:
        return True
