"""Zoom tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_zoom import streams


class TapZoom(Tap):
    """Zoom tap class."""

    name = "tap-zoom"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "account_id",
            th.StringType,
            required=True,
            secret=False,
            description="The token to authenticate against the API service",
        ),
        th.Property(
            "client_id",
            th.StringType,
            required=True,
            secret=False,
            description="OAuth application's Development or Production Client ID.",
        ),
        th.Property(
            "client_secret",
            th.StringType,
            required=True,
            secret=True,
            description="The token to authenticate against the API service",
        ),
        th.Property(
            "page_limit",
            th.IntegerType,
            default=300,
            description="The response limit for paginated streams.",
        ),
        th.Property(
            "auth_expiration",
            th.IntegerType,
            default=300,
            description="",
        ),
        th.Property(
            "api_url",
            th.StringType,
            description="Override the url for the API service.",
        ),
        th.Property(
            "stream_config",
            th.ArrayType(
                th.PropertiesList(
                    th.Property(
                        "stream",
                        th.StringType,
                        required=True,
                        description="Name of stream to apply a custom configuration.",
                    ),
                    th.Property(
                        "parameters",
                        th.StringType,
                        description=(
                            "URL formatted parameters string " "to be used for stream."
                        ),
                    ),
                ),
            ),
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.ZoomStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.UsersStream(self),
        ]


if __name__ == "__main__":
    TapZoom.cli()
