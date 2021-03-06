import requests
import os
import urllib


from typing import List
from .poller import Resort, WebsitePoller


RESORT_LIST = "https://account.ikonpass.com/api/v2/resorts"
RESORTS = {"Arapahoe Basin": "38", "Winter Park": "34"}
RESORT_AVAIL_URL = (
    "https://account.ikonpass.com/api/v2/reservation-availability/{resort_id}"
)

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
)


class IkonPoller(WebsitePoller):
    def __init__(self, username: str = None, password: str = None):
        self.logged_in = False
        self.s = None
        if username is None and password is None:
            username = os.environ["IKON_USERNAME"]
            password = os.environ["IKON_PASSWORD"]
        self.username = username
        self.password = password

    def _login(self):
        if self.logged_in:
            return
        self.s.headers.update({"User-Agent": USER_AGENT})
        payload = {
            "email": self.username,
            "password": self.password,
        }
        headers = {
            "Origin": "https://account.ikonpass.com",
            "referer": "https://account.ikonpass.com/en/login",
        }
        login_url = "https://account.ikonpass.com/session"
        # r = requests.put(login_url, headers=headers, json=payload)
        r = self.s.get("https://account.ikonpass.com/login", headers=headers)
        r.raise_for_status()
        r = self.s.get("https://account.ikonpass.com/ping", headers=headers)
        r.raise_for_status()
        # print(r.request.headers)
        token = urllib.parse.unquote(self.s.cookies["PROD-XSRF-TOKEN"])
        headers = {"X-CSRF-Token": token}

        r = self.s.put(login_url, headers=headers, json=payload)
        if r.status_code != 204:
            raise Exception(r)
        self.logged_in = True

    def poll(self, session: requests.Session = None) -> List[Resort]:
        if session is None:
            self.s = requests.Session()
        else:
            self.s = session
        if not self.logged_in:
            self._login()

        for resort_name, resort_id in RESORTS.items():
            req_url = RESORT_AVAIL_URL.format(resort_id=resort_id)
            res = self.s.get(req_url)
            res.raise_for_status()
            data = res.json()
            print(data)
        return None
