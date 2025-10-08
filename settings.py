# settings.py

from datetime import datetime, timezone


def get_current_utc_timestamp():
    """Returns a standardized timestamp for logging and email use."""
    return datetime.now(timezone.utc).isoformat()


if __name__ == "__main__":
    # Current timestamp
    cur_utc_timestamp = get_current_utc_timestamp()
    print('Current timestamp:', cur_utc_timestamp)
    