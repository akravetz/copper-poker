import requests
import os
import urllib
import json
import datetime as dt


from typing import List
from .poller import Resort, WebsitePoller


RESORT_LIST = "https://account.ikonpass.com/api/v2/resorts"
RESORTS = {"Arapahoe Basin": "38", "Winter Park": "34"}
RESORT_AVAIL_URL = (
    "https://account.ikonpass.com/api/v2/reservation-availability/{resort_id}"
)

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"

# api queries will return separate availability for each pass level (base pass, full pass, and day pass)
# we typically only want the base pass data
IKON_BASE_PASS_ID = 8973859


class IkonPoller(WebsitePoller):
    def __init__(self, username: str = None, password: str = None):
        self.logged_in = False
        if username is None and password is None:
            username = os.environ["IKON_USERNAME"]
            password = os.environ["IKON_PASSWORD"]
        self.username = username
        self.password = password

    def _login(self, session):
        if self.logged_in:
            return
        session.headers.update({"User-Agent": USER_AGENT})
        payload = {
            "email": self.username,
            "password": self.password,
        }
        headers = {
            "Origin": "https://account.ikonpass.com",
            "referer": "https://account.ikonpass.com/en/login",
        }
        login_url = "https://account.ikonpass.com/session"
        # replicate the login flow which is
        # login page -> ping -> extract CSRF token from ping -> login with extracted CSRF token
        r = session.get("https://account.ikonpass.com/login", headers=headers)
        r.raise_for_status()
        r = session.get("https://account.ikonpass.com/ping", headers=headers)
        r.raise_for_status()
        token = urllib.parse.unquote(session.cookies["PROD-XSRF-TOKEN"])
        headers = {"X-CSRF-Token": token}

        r = session.put(login_url, headers=headers, json=payload)
        if r.status_code != 204:
            raise Exception(r)
        self.logged_in = True

    def poll(self, session: requests.Session = None) -> List[Resort]:
        if session is None:
            session = requests.Session()

        if not self.logged_in:
            self._login(session)

        results = []
        # query availability for each resort in sequence
        for resort_name, resort_id in RESORTS.items():
            req_url = RESORT_AVAIL_URL.format(resort_id=resort_id)
            res = session.get(req_url)
            res.raise_for_status()
            data = res.json()["data"]
            # Ikon base pass availability only (id = 873859)
            base_pass_data = [d for d in data if d["id"] == IKON_BASE_PASS_ID]
            if len(base_pass_data) != 1:
                raise Exception("Unable to identify ikon base pass availability")
            base_pass_data = base_pass_data[0]

            # ikon is weird - instead of telling you available dates, you assume all dates are available
            # then it tells you which dates AREN'T available
            # so we create an array of 'all dates', then remove them from the list if ikon says they're not
            # available
            first_date = dt.datetime.now().date()
            all_dates = [first_date + dt.timedelta(days=n) for n in range(2 * 30)]
            unavail = (
                base_pass_data["unavailable_dates"] + base_pass_data["closed_dates"]
            )
            unavail = [
                dt.datetime.strptime(dt_str, "%Y-%m-%d").date() for dt_str in unavail
            ]
            avail_dates = [dt for dt in all_dates if dt not in unavail]
            results.append(Resort(name=resort_name, available_dates=avail_dates))

        return results

    def resort_names(self) -> List[str]:
        return list(RESORTS.keys())
