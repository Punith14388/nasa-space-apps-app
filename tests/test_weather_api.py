import base64
import json
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

from weather_api import (
    API_BASE_URL,
    WEATHER_PARAMETERS,
    WeatherAPIError,
    WeatherTelemetry,
    fetch_weather_telemetry,
)


def response_payload():
    readings = {
        "t_2m:C": 18.5,
        "relative_humidity_2m:p": 64.0,
        "wind_speed_10m:ms": 3.2,
        "precip_1h:mm": 0.1,
    }
    return {
        "data": [
            {
                "parameter": parameter,
                "coordinates": [{"dates": [{"date": "2026-11-13T21:00:00Z", "value": value}]}],
            }
            for parameter, value in readings.items()
        ]
    }


class FakeResponse:
    def __init__(self, body):
        self.body = body

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return None

    def read(self):
        return self.body


class FetchWeatherTelemetryTests(unittest.TestCase):
    @patch("weather_api.urlopen")
    def test_builds_authenticated_request_and_parses_weather(self, urlopen):
        urlopen.return_value = FakeResponse(json.dumps(response_payload()).encode())

        result = fetch_weather_telemetry(37.7749, -122.4194, username="user", password="secret")

        self.assertEqual(
            result,
            WeatherTelemetry(
                temperature_c=18.5,
                relative_humidity_pct=64.0,
                wind_speed_mps=3.2,
                precipitation_mm=0.1,
                observed_at="2026-11-13T21:00:00Z",
            ),
        )
        request = urlopen.call_args.args[0]
        self.assertEqual(
            request.full_url,
            f"{API_BASE_URL}/api/now/{','.join(WEATHER_PARAMETERS)}/37.7749,-122.4194/json",
        )
        expected_auth = base64.b64encode(b"user:secret").decode("ascii")
        self.assertEqual(request.get_header("Authorization"), f"Basic {expected_auth}")
        self.assertEqual(urlopen.call_args.kwargs["timeout"], 10.0)

    def test_requires_credentials(self):
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaisesRegex(WeatherAPIError, "credentials are required"):
                fetch_weather_telemetry(0, 0)

    def test_rejects_out_of_range_coordinates(self):
        with self.assertRaisesRegex(ValueError, "latitude must be between"):
            fetch_weather_telemetry(91, 0, username="user", password="secret")

    @patch("weather_api.urlopen")
    def test_rejects_incomplete_response(self, urlopen):
        payload = response_payload()
        payload["data"].pop()
        urlopen.return_value = FakeResponse(json.dumps(payload).encode())

        with self.assertRaisesRegex(WeatherAPIError, "all expected weather readings"):
            fetch_weather_telemetry(0, 0, username="user", password="secret")

    @patch("weather_api.urlopen")
    def test_surfaces_http_failures(self, urlopen):
        urlopen.side_effect = HTTPError("https://api.meteomatics.com", 401, "Unauthorized", {}, None)

        with self.assertRaisesRegex(WeatherAPIError, "HTTP 401"):
            fetch_weather_telemetry(0, 0, username="user", password="secret")


if __name__ == "__main__":
    unittest.main()
