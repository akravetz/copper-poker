from .utils import new_mock_session
from polls import CopperPoller


def test_coppper(mocker):
    mock_sess = new_mock_session(
        mocker,
        {
            "default": "{}",
        },
    )
    inst = CopperPoller(auth_token="FOO TOKEN")
    inst.poll(mock_sess)
