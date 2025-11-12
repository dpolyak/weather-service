# weather_service.py

import requests
import json
from settings import get_current_utc_timestamp, CityCoordinate
from dataclasses import dataclass
from typing import Optional
import logging
#from typing import Dict, Any


@dataclass(frozen=True)
class WeatherData:
    """Weather data returned by the external API."""
    time: str
    temp_celsius: float
    wind_speed_kph: float
    humidity: Optional[float] = None
    condition: Optional[str] = None


@dataclass(frozen=True)
class WeatherSnapshot:
    """Full weather record for a specific city and fetch cycle."""
    city_name: str
    latitude: float
    longitude: float
    fetched_at: str
    data: WeatherData
    source: str = "open-meteo"


# --- API Configuration ---
WEATHER_API_ENDPOINT = "https://api.open-meteo.com/v1/forecast"


class WeatherDataError(Exception):
    """Custom exception for API or parsing failures."""
    pass


def fetch_weather(city: CityCoordinate) -> WeatherData:
    """
    Fetch and parse current weather data for the specified city.

    Connects to the external weather API, retrieves the current temperature and wind speed,
    and returns parsed data as a WeatherData object.

    Args:
        city (CityCoordinate): CityCoordinate object with name, latitude, and longitude.

    Returns:
        WeatherData: Parsed weather data object.

    Raises:
        WeatherDataError: If the API call fails, the response is malformed,
                          or required data is missing.

    Functional Requirements:
        FR-AWN-001: Securely connect to the designated external weather API.
        FR-AWN-003: Extract specific metrics (temperature, wind speed).
    """
    logger = logging.getLogger(__name__)
    logger.info(f"[{get_current_utc_timestamp()}] Attempting to fetch weather data for {city.name}...")

    params = {
        'latitude': city.latitude,
        'longitude': city.longitude,
        'current': 'temperature_2m,wind_speed_10m',
        'timezone': 'America/New_York'
    }
    try:
        # FR-AWN-001: Securely connect to the designated external weather API
        response = requests.get(WEATHER_API_ENDPOINT, params=params, timeout=10)
        response.raise_for_status()
        raw_data = response.json()

        logger.debug("Raw weather API response: %r", raw_data)

        # Validate the structure of the response (FR-AWN-003)
        current = raw_data.get('current')
        if not isinstance(current, dict):
            raise WeatherDataError("API Response Parsing Error: 'current' section missing or not a dict.")

        # Extract required fields, fail gracefully if missing
        try:
            time_val = current['time']
            temp_celsius = current['temperature_2m']
            wind_speed_kph = current['wind_speed_10m']
        except KeyError as e:
            raise WeatherDataError(f"API Response Parsing Error: Missing key {e} in 'current' section.")

        weather_data = WeatherData(
            time=time_val,
            temp_celsius=temp_celsius,
            wind_speed_kph=wind_speed_kph
        )

        logger.info(f"[{get_current_utc_timestamp()}] Data successfully fetched and parsed for {city.name}.")
        return weather_data

    except requests.exceptions.RequestException as exc:
        logger.error("API Connection or HTTP Error: %s", exc)
        raise WeatherDataError(f"API Connection or HTTP Error: {exc}") from exc
    except WeatherDataError as exc:
        logger.error(str(exc))
        raise
    except Exception as exc:
        logger.exception("An unexpected error occurred during fetching.")
        raise WeatherDataError(f"An unexpected error occurred during fetching: {exc}") from exc
    

if __name__ == "__main__":
    from settings import CITIES_COORDINATES
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.WARNING)

    city = CityCoordinate("Toronto", 43.6532, -79.3832)

    logger.info(f"Fetching weather for {city.name}")
    weather_data = fetch_weather(city)
    current_time = get_current_utc_timestamp()
    logger.info(f"Weather data for {city.name}: {weather_data}")

    weather_snapshot = WeatherSnapshot(
        city_name = city.name,
        latitude = city.latitude,
        longitude = city.longitude,
        fetched_at = current_time,
        data = weather_data
    )

    print(weather_snapshot)
    