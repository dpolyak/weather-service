# storage_service.py

import sqlite3
import json
from dataclasses import asdict
from pathlib import Path
from weather_client import WeatherSnapshot


# --- Configuration ---
DB_PATH = Path("weather.db")
JSON_LOG_PATH = Path("weather_log.json")


# --- SQLite setup and storage ---
def save_to_sqlite(snapshot: WeatherSnapshot) -> None:
    """
    Save a WeatherSnapshot record to the local SQLite database.
    Creates the database and table if they don't exist.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather (
        city_name TEXT,
        latitude REAL,
        longitude REAL,
        fetched_at TEXT,
        time TEXT,
        temp_celsius REAL,
        wind_speed_kph REAL,
        humidity REAL,
        condition TEXT,
        source TEXT
    )
    """)

    cursor.execute("""
    INSERT INTO weather VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        snapshot.city_name,
        snapshot.latitude,
        snapshot.longitude,
        snapshot.fetched_at,
        snapshot.data.time,
        snapshot.data.temp_celsius,
        snapshot.data.wind_speed_kph,
        snapshot.data.humidity,
        snapshot.data.condition,
        getattr(snapshot, "source", "open-meteo"),
    ))

    conn.commit()
    conn.close()


# --- JSON log storage ---
def save_to_json(snapshot: WeatherSnapshot) -> None:
    """
    Append a WeatherSnapshot record to a JSON log file.
    Each entry is stored on a separate line for easy incremental writes.
    """
    record = asdict(snapshot)
    with open(JSON_LOG_PATH, "a", encoding="utf-8") as f:
        json.dump(record, f)
        f.write("\n")


# --- Unified interface ---
def persist_weather(snapshot: WeatherSnapshot) -> None:
    """
    Save a weather snapshot to both SQLite and JSON.
    """
    save_to_sqlite(snapshot)
    save_to_json(snapshot)