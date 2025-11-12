# weather_collector_app.py

from flask import Flask, jsonify
#from weather_collector import run_weather_collection
from settings import CITIES_COORDINATES, CityCoordinate, get_current_utc_timestamp
from weather_client import fetch_weather, WeatherSnapshot
import logging

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

@app.route("/", methods=["GET"])
def collect_weather():
    try:
        all_snapshots = []
        logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.WARNING)
        
        city = CityCoordinate("Toronto", 43.6532, -79.3832)
        for city in CITIES_COORDINATES:

            logger.info(f"Fetching weather for {city.name}")
            weather_data = fetch_weather(city)
            current_time = get_current_utc_timestamp()
            logger.info(f"Weather data for {city.name}: {weather_data}")

            # weather_snapshot = WeatherSnapshot(
            #     city_name = city.name,
            #     latitude = city.latitude,
            #     longitude = city.longitude,
            #     fetched_at = current_time,
            #     data = weather_data
            # )

            weather_snapshot = {'city_name' : city.name,
                                'data' : {'temp_celsius' : weather_data.temp_celsius,
                                          'wind_speed_kph' : weather_data.wind_speed_kph,
                                        }
                               }

            all_snapshots.append(weather_snapshot)

        return jsonify(all_snapshots), 200
    except Exception as e:
        logging.error(f"Error during weather collection: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    # Local test
    app.run(host="0.0.0.0", port=8080, debug=True)