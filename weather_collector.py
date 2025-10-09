from weather_client import fetch_weather, WeatherSnapshot, CITIES_COORDINATES
from settings import get_current_utc_timestamp
from storage_service import persist_weather
import logging

logging.basicConfig(level=logging.INFO)

def run_weather_collection():
    snapshots_saved = 0
    for city in CITIES_COORDINATES:
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
    return {"status": "success", "items_collected": snapshots_saved}

if __name__ == "__main__":
    result = run_weather_collection()
    logging.info(result)