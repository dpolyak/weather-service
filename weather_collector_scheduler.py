# scheduler.py
import schedule
import time
from weather_collector import run_weather_collector

RUN_INTERVAL_MINUTES = 15

def job():
    print("⏰ Running weather collector...")
    run_weather_collector()

schedule.every(RUN_INTERVAL_MINUTES).minutes.do(job)

if __name__ == "__main__":
    print("🌀 Weather scheduler started (every {RUN_INTERVAL_MINUTES} min)...")
    while True:
        schedule.run_pending()
        time.sleep(60)