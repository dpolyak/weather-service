#weather_collector.py

from weather_client import fetch_weather, WeatherSnapshot
from settings import get_current_utc_timestamp, CITIES_COORDINATES
from storage_service import persist_weather
import logging

logging.basicConfig(level=logging.INFO)

def run_weather_collection():
    snapshots_saved = 0
    for city in CITIES_COORDINATES:
        try:
            data = fetch_weather(city)
            snapshot = WeatherSnapshot(
                city_name=city.name,
                latitude=city.latitude,
                longitude=city.longitude,
                fetched_at=get_current_utc_timestamp(),
                data=data
            )
            persist_weather(snapshot)
            snapshots_saved += 1
            logging.info(f"✅ Stored weather snapshot for {city.name}")
        except Exception as e:
            logging.error(f"❌ Failed to process {city.name}: {e}")
    return {"status": "success", "items_collected": snapshots_saved}


if __name__ == "__main__":
    result = run_weather_collection()
    logging.info(result)