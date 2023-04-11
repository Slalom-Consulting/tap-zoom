"""Mock API."""

import json

import requests_mock

API_URL = "https://api.zoom.us/v2"
AUTH_URL = "https://zoom.us/oauth/token"

mock_responses_path = "tests/mock_responses"

mock_responses = {
    "auth": {
        "type": "auth",
        "url": AUTH_URL,
        "file": "auth.json",
    },
    "users": {
        "type": "stream",
        "endpoint": "/users",
        "file": "users.json",
    }
}


def mock_api(func, SAMPLE_CONFIG):
    """Mock API."""

    def wrapper():
        with requests_mock.Mocker() as m:
            for k, v in mock_responses.items():
                path = f"{mock_responses_path}/{v['file']}"

                if v["type"] == "auth":
                    url = v["url"]

                    with open(path, "r") as f:
                        response = json.load(f)

                    m.post(url, json=response)

                elif v["type"] == "stream":
                    url = f"{API_URL}{v['endpoint']}"

                    with open(path, "r") as f:
                        response = json.load(f)

                    m.get(url, json=response)

            func()

    wrapper()
