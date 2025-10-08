# scheduler.py
import schedule
import time
from weather_collector import run_weather_collector

def job():
    print("⏰ Running weather collector...")
    run_weather_collector()

schedule.every(15).minutes.do(job)

if __name__ == "__main__":
    print("🌀 Weather scheduler started (every 15 min)...")
    while True:
        schedule.run_pending()
        time.sleep(60)