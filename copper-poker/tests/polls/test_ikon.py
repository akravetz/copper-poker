from polls import IkonPoller
from .utils import new_mock_session


def test_ikon(mocker):
    mock_sess = new_mock_session(
        mocker,
        {
            "default": "{}",
        },
    )
    mock_sess.cookies = {"PROD-XSRF-TOKEN": "MOCK_TOKEN"}
    inst = IkonPoller(username="FOO", password="BAR")
    inst.poll(mock_sess)
