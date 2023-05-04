""""""

from __future__ import annotations

# import jwt
from singer_sdk.authenticators import OAuthAuthenticator, SingletonMeta

# from singer_sdk.helpers._util import utc_now
# from singer_sdk.streams import Stream as RESTStreamBase

MAX_EXPIRATION = 60 * 60 * 24
AUTH_URL = "https://zoom.us/oauth/token"


# class ZoomJWTAuthenticator(OAuthAuthenticator):
#    """(Depricated) JWT Authentication for the Zoom API
#
#    End of support for this method is secheduled for June 1, 2023. Visit
#    [here](https://marketplace.zoom.us/docs/guides/build/jwt-app/jwt-faq/)
#    for more details.
#    """
#
#    def __init__(
#        self, stream: RESTStreamBase, default_expiration: int | None = None
#    ) -> None:
#        auth_endpoint = None
#        oauth_scopes = None
#
#        if default_expiration and default_expiration > MAX_EXPIRATION:
#            default_expiration = MAX_EXPIRATION
#
#        super().__init__(stream, auth_endpoint, oauth_scopes, default_expiration)
#
#    # Authentication and refresh
#    def update_access_token(self) -> None:
#        """Update `access_token` along with: `last_refreshed` and `expires_in`."""
#
#        request_time = utc_now()
#        expiry_time = request_time.add(seconds=self._default_expiration).int_timestamp
#
#        payload = {"iss": self.client_id, "exp": expiry_time}
#
#        self.access_token = jwt.encode(payload, self.client_secret, "HS256")
#        self.expires_in = self._default_expiration
#        self.last_refreshed = request_time


class ZoomOAuthAuthenticator(OAuthAuthenticator, metaclass=SingletonMeta):
    @property
    def auth_endpoint(self) -> str:
        return self.config.get("auth_url", AUTH_URL)

    @property
    def oauth_request_body(self) -> dict:
        """Get formatted body of the OAuth authorization request."""

        return {
            "grant_type": "account_credentials",
            "account_id": self.config.get("account_id"),
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
