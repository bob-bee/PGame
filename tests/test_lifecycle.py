import pytest
from unittest.mock import patch
from federation import webfinger

@pytest.fixture
def mock_webfinger_response():
    return {
        "subject": "acct:user@example.com",
        "aliases": ["http://example.com/user"],
        "links": [
            {"rel": "self", "href": "https://example.com/user"},
            {"rel": "http://webfinger.net/rel/avatar", "type": "image/png", "href": "http://example.com/avatar.png"}
        ]
    }

@patch('federation.webfinger.requests.get')
def test_webfinger(mock_get, mock_webfinger_response):
    mock_get.return_value.json.return_value = mock_webfinger_response
    response = webfinger.fetch_user_info('user@example.com', 'example.com')
    assert response == {
        "subject": "acct:user@example.com",
        "aliases": ["http://example.com/user"],
        "links": [
            {"rel": "self", "href": "https://example.com/user"},
            {"rel": "http://webfinger.net/rel/avatar", "type": "image/png", "href": "http://example.com/avatar.png"}
        ]
    }