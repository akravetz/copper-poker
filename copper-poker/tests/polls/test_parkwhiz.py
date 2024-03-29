from .utils import new_mock_session
from polls import CopperPoller, EldoraPoller


def test_coppper(mocker):
    mock_sess = new_mock_session(
        mocker,
        [
            {"url": "default", "response": "{}"},
        ],
    )
    inst = CopperPoller(bearer_token="FOO TOKEN")
    inst.poll(mock_sess)


def test_eldora(mocker):
    mock_sess = new_mock_session(
        mocker,
        [
            {"url": "default", "response": "{}"},
        ],
    )
    inst = EldoraPoller(bearer_token="FOO TOKEN")
    inst.poll(mock_sess)
