"""Stream type classes for tap-zoom."""

from __future__ import annotations

from pathlib import Path

from tap_zoom.client import ZoomStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class UsersStream(ZoomStream):
    """List users stream."""

    # https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/users
    # Scopes: user:read:admin
    # rate limit: Medium
    # max page size:  page_size = 300

    name = "users"
    path = "/users"
    primary_keys = ["id"]
    replication_key = None
    records_jsonpath = "$.users[*]"
    schema_filepath = SCHEMAS_DIR / "users.json"
