class Item:
    def __init__(self, id, name, description, status='To Do'):
        self.id = id
        self.name = name
        self.description = description
        self.status = status

    @classmethod
    def from_mongo_item(cls, item):
        return cls(item["_id"], item["name"], item["desc"], item["status"])
