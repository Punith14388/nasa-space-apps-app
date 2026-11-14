"""Meteomatics weather telemetry client."""

from __future__ import annotations

import base64
import json
import math
import os
from dataclasses import dataclass
from numbers import Real
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

API_BASE_URL = "https://api.meteomatics.com"
WEATHER_PARAMETERS = (
    "t_2m:C",
    "relative_humidity_2m:p",
    "wind_speed_10m:ms",
    "precip_1h:mm",
)


class WeatherAPIError(RuntimeError):
    """Raised when Meteomatics credentials or a weather response are invalid."""


@dataclass(frozen=True)
class WeatherTelemetry:
    """Current weather values returned by Meteomatics for a location."""

    temperature_c: float
    relative_humidity_pct: float
    wind_speed_mps: float
    precipitation_mm: float
    observed_at: str


def fetch_weather_telemetry(
    latitude: float,
    longitude: float,
    *,
    username: str | None = None,
    password: str | None = None,
    timeout: float = 10.0,
) -> WeatherTelemetry:
    """Fetch current weather for coordinates using Meteomatics Basic Auth.

    Credentials default to the METEOMATICS_USERNAME and METEOMATICS_PASSWORD
    environment variables.
    """
    latitude = _validate_coordinate(latitude, "latitude", -90.0, 90.0)
    longitude = _validate_coordinate(longitude, "longitude", -180.0, 180.0)
    if isinstance(timeout, bool) or not isinstance(timeout, Real) or not math.isfinite(timeout) or timeout <= 0:
        raise ValueError("timeout must be a positive finite number")

    username = os.environ.get("METEOMATICS_USERNAME") if username is None else username
    password = os.environ.get("METEOMATICS_PASSWORD") if password is None else password
    if not username or not password:
        raise WeatherAPIError(
            "Meteomatics credentials are required; set METEOMATICS_USERNAME and METEOMATICS_PASSWORD."
        )

    location = f"{latitude:.15g},{longitude:.15g}"
    parameters = ",".join(WEATHER_PARAMETERS)
    url = f"{API_BASE_URL}/api/now/{parameters}/{location}/json"
    token = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")
    request = Request(url, headers={"Authorization": f"Basic {token}", "Accept": "application/json"})

    try:
        with urlopen(request, timeout=float(timeout)) as response:
            payload = json.loads(response.read())
    except HTTPError as error:
        raise WeatherAPIError(f"Meteomatics returned HTTP {error.code}.") from error
    except URLError as error:
        raise WeatherAPIError(f"Unable to reach Meteomatics: {error.reason}") from error
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise WeatherAPIError("Meteomatics returned invalid JSON.") from error

    return _parse_telemetry(payload)


def _validate_coordinate(value: float, name: str, minimum: float, maximum: float) -> float:
    if isinstance(value, bool) or not isinstance(value, Real) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number")
    if not minimum <= value <= maximum:
        raise ValueError(f"{name} must be between {minimum:g} and {maximum:g}")
    return float(value)


def _parse_telemetry(payload: object) -> WeatherTelemetry:
    if not isinstance(payload, dict) or not isinstance(payload.get("data"), list):
        raise WeatherAPIError("Meteomatics response is missing its data list.")

    values: dict[str, float] = {}
    observed_at: str | None = None
    for item in payload["data"]:
        if not isinstance(item, dict):
            continue
        parameter = item.get("parameter")
        coordinates = item.get("coordinates")
        if parameter not in WEATHER_PARAMETERS or not isinstance(coordinates, list) or not coordinates:
            continue
        coordinate = coordinates[0]
        dates = coordinate.get("dates") if isinstance(coordinate, dict) else None
        if not isinstance(dates, list) or not dates or not isinstance(dates[0], dict):
            continue
        reading = dates[0]
        value = reading.get("value")
        date = reading.get("date")
        if isinstance(value, bool) or not isinstance(value, Real) or not math.isfinite(value):
            continue
        values[parameter] = float(value)
        if observed_at is None and isinstance(date, str):
            observed_at = date

    if len(values) != len(WEATHER_PARAMETERS) or observed_at is None:
        raise WeatherAPIError("Meteomatics response did not contain all expected weather readings.")

    return WeatherTelemetry(
        temperature_c=values["t_2m:C"],
        relative_humidity_pct=values["relative_humidity_2m:p"],
        wind_speed_mps=values["wind_speed_10m:ms"],
        precipitation_mm=values["precip_1h:mm"],
        observed_at=observed_at,
    )
