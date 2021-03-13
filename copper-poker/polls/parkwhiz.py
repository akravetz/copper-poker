from typing import List
import os
import datetime as dt
import requests
from .poller import Resort, WebsitePoller

API_URL = "https://api.parkwhiz.com/v4/venues/{venue_id}/events/?fields=%3Adefault%2Csite_url%2Cavailability%2Cvenue%3Atimezone&q=%20starting_after%3A2021-01-03T00%3A00%3A00-07%3A00&sort=start_time&zoom=pw%3Avenue"


class ParkwhizPoller(WebsitePoller):
    def __init__(self, venue_name: str, venue_id: str, bearer_token: str):
        self.venue_name = venue_name
        self.venue_id = venue_id
        self.bearer_token = bearer_token

    def poll(self, session: requests.Session = None) -> List[Resort]:
        if session is None:
            session = requests.Session()
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
            "Authorization": f"Bearer {self.bearer_token}",
        }
        r = session.get(
            API_URL.format(venue_id=self.venue_id), data=data, headers=headers
        )
        r.raise_for_status()
        js = r.json()

        avail_dates = []
        for itm in js:
            park_dt = dt.datetime.strptime(itm["start_time"], "%Y-%m-%dT%H:%M:%S.%f%z")
            if park_dt.hour > 10:
                # don't care about parking slots that start after 10am
                continue
            park_slots = int(itm["availability"]["available"])
            if park_slots > 0:
                avail_dates.append(park_dt.date())
        return [Resort(name=self.venue_name, available_dates=avail_dates)]
