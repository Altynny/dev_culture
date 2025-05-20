import pytest
from unittest.mock import patch

from services import get_users, get_files

@patch('services.requests.get')
def test_get_users(mock_get):
    mock_get.return_value.ok = True

    response = get_users()

    assert response is not None

@patch('services.requests.get')
def test_get_files(mock_get):
    mock_get.return_value.ok = True

    response = get_files()

    assert response is not None