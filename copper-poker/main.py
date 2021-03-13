import datetime as dt
from twilio.rest import Client
from polls import CopperPoller, IkonPoller, EldoraPoller
import requests
import os
import json
import time

# your account sid from twilio.com/console
SLEEP_SECS = 5

TWILIO_ACCOUNT = os.environ["TWILIO_ACCOUNT"]
TWILIO_TOKEN = os.environ["TWILIO_TOKEN"]
TWILIO_NUMBER = os.environ["TWILIO_NUMBER"]

client = Client(TWILIO_ACCOUNT, TWILIO_TOKEN)


def main():
    text_resorts = {}
    dates_of_interest = {"Eldora": [dt.date(2021, 3, 14), dt.date(2021, 3, 24)]}
    pollers = [EldoraPoller()]  # [IkonPoller(), CopperPoller()]
    s = requests.Session()
    while True:
        results = []
        for poller in pollers:
            res = poller.poll(s)
            results.extend(res)

        for resort in results:
            dates = dates_of_interest.get("any", [])
            dates = dates + dates_of_interest.get(resort.name, [])
            for test_dt in dates:
                if (
                    test_dt in resort.available_dates
                    and test_dt not in text_resorts.get(resort.name, [])
                ):
                    client.messages.create(
                        to="+18133168561",
                        from_=TWILIO_NUMBER,
                        body=f"reservation available for {resort.name} on {test_dt}",
                    )
                    curr = text_resorts.get(resort.name, [])
                    curr.append(test_dt)
                    text_resorts[resort.name] = curr
        time.sleep(SLEEP_SECS)


if __name__ == "__main__":
    main()
