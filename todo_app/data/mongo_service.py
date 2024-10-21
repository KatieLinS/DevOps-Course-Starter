import pymongo
import os
from bson.objectid import ObjectId
from todo_app.data.status_enum import Status
from todo_app.data.item import Item


class MongoService():
    def __init__(self):
        self.client = pymongo.MongoClient(os.environ.get('MONGOBD_PRIMARY_CONNECTION_STRING'))
        self.db = self.client[os.environ.get('MONGO_DATABASE_NAME')]
        self.collection = self.db[os.environ.get('MONGO_COLLECTION_NAME')]

    def get_items(self):
        items = []

        for item in self.collection.find():
            items.append(Item.from_mongo_item(item))

        return items

    def add_item(self, title):
        self.collection.insert_one({
            'name': title,
            'desc': "",
            "status": Status.TODO.value
        })

    def move_item_to_list(self, id, new_status):
        self.collection.update_one({'_id': ObjectId(id)}, {
            "$set": {'status': new_status}})
