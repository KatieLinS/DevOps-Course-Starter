import os
import pytest
import pymongo
import mongomock
from dotenv import load_dotenv, find_dotenv
from todo_app import app
from todo_app.data.status_enum import Status
from flask_dance.consumer.storage import MemoryStorage
from todo_app.oauth import blueprint


@pytest.fixture
def client(monkeypatch):
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        # Create the new app.
        test_app = app.create_app()

        storage = MemoryStorage({"access_token": "fake-token"})
        monkeypatch.setattr(blueprint, 'storage', storage)

        # Use the app to create a test_client that can be used in our tests.
        with test_app.test_client() as client:
            yield client

def test_index_page(client):
    # Arrange
    mongo_client = pymongo.MongoClient(os.environ.get('MONGOBD_PRIMARY_CONNECTION_STRING'))
    db = mongo_client[os.environ.get('MONGO_DATABASE_NAME')]
    collection = db[os.environ.get('MONGO_COLLECTION_NAME')]

    collection.insert_one({
        'name': 'Test item',
        'desc': "",
        "status": Status.TODO.value
    })

    # Act
    response = client.get('/')

    # Assert
    assert response.status_code == 200
    assert 'Test item' in response.data.decode()
