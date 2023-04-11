"""Tests standard tap features using the built-in SDK tests library."""

from singer_sdk.testing import get_standard_tap_tests

from tap_zoom.tap import TapZoom
from tests.mock_api import mock_api


SAMPLE_CONFIG = {
    "account_id": "test",
    "client_id": "test",
    "client_secret": "test"
}


# Run standard built-in tap tests from the SDK:
def test_standard_tap_tests():
    """Run standard tap tests from the SDK."""
    tests = get_standard_tap_tests(TapZoom, config=SAMPLE_CONFIG)
    for test in tests:
        if test.__name__ in ("_test_stream_connections"):
            mock_api(test, SAMPLE_CONFIG)
            continue

        test()

test_standard_tap_tests()