import datetime as dt
from twilio.rest import Client
from polls import CopperPoller, IkonPoller
import os
import json
import time

# your account sid from twilio.com/console
SLEEP_SECS = 100

TWILLIO_ACCOUNT = os.environ["TWILLIO_ACCOUNT"]
TWILLIO_TOKEN = os.environ["TWILLIO_TOKEN"]

client = Client(TWILLIO_ACCOUNT, TWILLIO_TOKEN)


def main():
    pollers = [IkonPoller()]  # [CopperPoller()]  # , IkonPoller()]
    while True:
        results = []
        for poller in pollers:
            res = poller.poll()
            results.append(res)
        time.sleep(SLEEP_SECS)


if __name__ == "__main__":
    main()
