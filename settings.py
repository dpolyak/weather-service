# settings.py

from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass(frozen=True)
class CityCoordinate:
    """Represents the geographic location of a tracked city."""
    name: str
    latitude: float
    longitude: float

CITIES_COORDINATES = [
    CityCoordinate("Toronto", 43.6532, -79.3832),
    CityCoordinate("Montreal", 45.5017, -73.5673),
    CityCoordinate("Tel Aviv", 32.0853, 34.7818),
    CityCoordinate("Haifa", 32.7940, 34.9896),
    CityCoordinate("Kyiv", 50.4501, 30.5234),
    CityCoordinate("Lviv", 49.8397, 24.0297),
    CityCoordinate("New York", 40.7128, -74.0060),
]

# Function to get UTC timestamp
def get_current_utc_timestamp():
    return datetime.now(timezone.utc).isoformat()


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)

    logging.info('Current UTC timestamp: %s', get_current_utc_timestamp())
    logging.info('Tracked cities:')
    for city in CITIES_COORDINATES:
        logging.info(" - %s: (%f, %f)", city.name, city.latitude, city.longitude)