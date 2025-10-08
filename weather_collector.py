from weather_client import fetch_weather, WeatherSnapshot, CITIES_COORDINATES
from settings import get_current_utc_timestamp
from storage_service import persist_weather

def run_weather_collector():
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
        print(f"✅ Stored weather snapshot for {city.name}")

if __name__ == "__main__":
    run_weather_collector()