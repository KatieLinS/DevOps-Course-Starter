import os
import pytest
import requests
from dotenv import load_dotenv, find_dotenv
from todo_app import app


@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    # Create the new app.
    test_app = app.create_app()

    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client


class StubResponse():
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data

    def json(self):
        return self.fake_response_data


def stub(action, url, headers={},  params={}):
    test_board_id = os.environ.get('BOARD_ID')

    if url == f'https://api.trello.com/1/boards/{test_board_id}/lists':
        fake_response_data = [{
            'id': '123abc',
            'name': 'To Do',
            'cards': [{'id': '456', 'name': 'Test card', 'desc': 'Test desc'}]
        }]
        return StubResponse(fake_response_data)

    raise Exception(f'Integration test did not expect URL "{url}"')


def test_index_page(monkeypatch, client):
    # Arrange
    monkeypatch.setattr(requests, 'request', stub)

    # Act
    response = client.get('/')

    # Assert
    assert response.status_code == 200
    assert 'Test card' in response.data.decode()
