import json
from polls import IkonPoller
from .utils import new_mock_session


def test_ikon(mocker):
    mock_data = {
        "data": [
            {
                "id": 8973859,
                "closed_dates": ["2021-01-01"],
                "unavailable_dates": ["2021-06-01"],
            }
        ]
    }
    mock_sess = new_mock_session(
        mocker,
        {
            "default": "{}",
            "https://account.ikonpass.com/api/v2/reservation-availability/38": json.dumps(mock_data),
            "https://account.ikonpass.com/api/v2/reservation-availability/34": json.dumps(mock_data)
        },
    )
    mock_sess.cookies = {"PROD-XSRF-TOKEN": "MOCK_TOKEN"}
    inst = IkonPoller(username="FOO", password="BAR")
    inst.poll(mock_sess)
