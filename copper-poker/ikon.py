import requests
import os
import urllib

IKON_USERNAME = os.environ["IKON_USERNAME"]
IKON_PASSWORD = os.environ["IKON_PASSWORD"]

RESORT_LIST = "https://account.ikonpass.com/api/v2/resorts"
ABASIN_AVAIL = "https://account.ikonpass.com/api/v2/reservation-availability/38"
WP_AVAIL = "https://account.ikonpass.com/api/v2/reservation-availability/34"


def main():
    payload = {
        "email": IKON_USERNAME,
        "password": IKON_PASSWORD,
    }
    headers = {
        "Origin": "https://account.ikonpass.com",
        "referer": "https://account.ikonpass.com/en/login",
    }
    login_url = "https://account.ikonpass.com/session"
    s = requests.Session()
    s.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        }
    )
    # r = requests.put(login_url, headers=headers, json=payload)
    r = s.get("https://account.ikonpass.com/login", headers=headers)
    r.raise_for_status()
    r = s.get("https://account.ikonpass.com/ping", headers=headers)
    r.raise_for_status()
    # print(r.request.headers)
    token = urllib.parse.unquote(s.cookies["PROD-XSRF-TOKEN"])
    headers = {"X-CSRF-Token": token}

    r = s.put(login_url, headers=headers, json=payload)
    if r.status_code != 204:
        raise Exception(r)


if __name__ == "__main__":
    main()
