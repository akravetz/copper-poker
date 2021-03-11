import requests
import json


def new_mock_session(mocker, response_map):
    """
    returns a new mock requests.Session which returns pre-canned responses for given URLs.
    response map should be a dictionary where they key is the URL and the value is the response to return for that URL
    The responses can be either strings or bytes
    """
    s = requests.Session()
    mock_session = mocker.Mock(s)

    mock_responses = {}

    # for each response buffer, return a new mock response each mock response
    # has the  and  properties mocked out to return our mock
    # data
    for url, mock_data in response_map.items():
        mock_response = mocker.Mock(requests.Response)
        mock_text = mocker.PropertyMock()
        mock_bytes = mocker.PropertyMock()

        if isinstance(mock_data, str):
            # if the user provides a string, then we mock both the
            # (string) and  (bytes) attribute of the response
            mock_text.return_value = mock_data
            mock_bytes.return_value = bytes(mock_data, "utf-8")
            mock_response.json.side_effect = lambda: json.loads(mock_data)

        elif isinstance(mock_data, bytes):
            # if the user provides bytes, then we only mock the
            # (bytes) attribute of the response
            mock_bytes.return_value = mock_data
            # bytes cant necessarily decode to UTF 8, blank text
            mock_text.return_value = ""
        else:
            raise TypeError("expected string or bytes result")

        # see second example of PropertyMock here:
        # https://docs.python.org/3/library/unittest.mock.html#unittest.mock.PropertyMock
        # TL;DR:  and  are properties of the requests.Response
        # object.  this is how one mocks properties of objects
        type(mock_response).text = mock_text
        type(mock_response).content = mock_bytes
        mock_response.status_code = 204
        mock_responses[url] = mock_response

    def mock_get(url, headers=None, json=None, data=None):
        if url not in mock_responses:
            return mock_responses["default"]
        return mock_responses[url]

    mock_session.get.side_effect = mock_get
    mock_session.put.side_effect = mock_get
    return mock_session
