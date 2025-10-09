# weather_collector_app.py

from flask import Flask, jsonify
from weather_collector import run_weather_collection
import logging

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

@app.route("/", methods=["GET"])
def collect_weather():
    try:
        result = run_weather_collection()
        return jsonify(result), 200
    except Exception as e:
        logging.error(f"Error during weather collection: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    # Local test
    app.run(host="0.0.0.0", port=8080, debug=True)