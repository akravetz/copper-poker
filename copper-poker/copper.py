import datetime as dt
import time
import requests
from twilio.rest import Client
import os

# your account sid from twilio.com/console
SLEEP_SECS = 1

TWILLIO_ACCOUNT = os.environ["TWILLIO_ACCOUNT"]
TWILLIO_TOKEN = os.environ["TWILLIO_TOKEN"]
COPPER_AUTH_TOKEN = os.environ["COPPER_AUTH_TOKEN"]
DESTINATION_NUMBER = os.environ['COPPER_DESTINATION_NUMBER']

client = Client(TWILLIO_ACCOUNT, TWILLIO_TOKEN)

API_URL = "https://api.parkwhiz.com/v4/venues/448854/events/?fields=%3Adefault%2Csite_url%2Cavailability%2Cvenue%3Atimezone&q=%20starting_after%3A2021-01-03T00%3A00%3A00-07%3A00&sort=start_time&zoom=pw%3Avenue"


def main():
    next_day = dt.timedelta(days=1)
    tomorrow = dt.datetime.now() + next_day
    tomorrow.strftime("%Y-%m-%d")
    data = {
        "fields": ":default,site_url,availability,venue:timezone",
        "q": f"starting_after:{tomorrow}T00:00:00-07:00",
        "sort": "start_time",
        "zoom": "pw:venue",
    }
    headers = {
        "Referer": "https://widget.arrive.com/",
        "Origin": "https://widget.arrive.com",
        "Authorization": f"Bearer {COPPER_AUTH_TOKEN}",
    }
    messages = {}
    TEST = True
    while True:
        time.sleep(SLEEP_SECS)
        r = requests.get(API_URL, data=data, headers=headers)
        r.raise_for_status()
        js = r.json()
        for itm in js:
            park_dt = dt.datetime.strptime(itm["start_time"][0:10], "%Y-%m-%d").date()
            park_slots = int(itm["availability"]["available"])
            is_weekend = park_dt.weekday() == 5 or park_dt.weekday() == 6
            if (is_weekend and park_slots > 0) or TEST:
                TEST = False
                msg = (
                    "%s is available (%d slots)\nbook here: https://tinyurl.com/parkcopper"
                    % (park_dt, park_slots)
                )
                date_str = str(park_dt)
                if date_str not in messages:
                    messages[date_str] = 1
                    message = client.messages.create(
                        to=DESTINATION_NUMBER, from_="+19382536768", body=msg
                    )

    # print(js)


if __name__ == "__main__":
    main()
