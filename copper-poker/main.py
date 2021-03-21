import datetime as dt
from collections import defaultdict
import requests
import os
import json
import time
import argparse
from twilio.rest import Client
from polls import CopperPoller, IkonPoller, EldoraPoller


# your account sid from twilio.com/console
SLEEP_SECS = 5

TWILIO_ACCOUNT = os.environ["TWILIO_ACCOUNT"]
TWILIO_TOKEN = os.environ["TWILIO_TOKEN"]
TWILIO_NUMBER = os.environ["TWILIO_NUMBER"]

client = Client(TWILIO_ACCOUNT, TWILIO_TOKEN)


def parse_args():
    parser = argparse.ArgumentParser(
        description="text notifications for open reservations at ikon ski resorts"
    )
    parser.add_argument("--phone-number", "-pn", required=True)
    parser.add_argument(
        "--date",
        "-dt",
        action="append",
        help="example: --date 'Araphoe Basin:2021-03-16'\n" "you can also pass `any` as the resort name to find availability at any resort",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    text_resorts = {}

    # parse dates that the user wants, these are passed in the form of a list of strings
    # where strings are:
    # Resort Name:YYYY-MM-DD
    dates_of_interest = defaultdict(list)
    for dt_arg in args.date:
        resort, dt = dt_arg.split(":")
        parsed_dt = dt.datetime.strptime(dt, "%Y-%m-%d").date()
        dates_of_interest[resort].append(parsed_dt)
    pollers = [IkonPoller(), CopperPoker(), EldoraPoker()]
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
