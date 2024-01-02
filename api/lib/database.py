from pymongo import MongoClient
from bson import json_util
import json


class Database:

    def __init__(self, url="mongodb", mongo_user='admin', mongo_pass='password') -> None:

        self._url = url
        self._mongo_user = mongo_user
        self._mongo_pass = mongo_pass

        return
    
    def _connect(self):
        
        client = MongoClient(self._url,
                             username=self._mongo_user,
                             password=self._mongo_pass,
                            )

        return client 
    
    def get_collection(self, db_name: str, collection: str):
        
        client = self._connect()
        db = client[db_name]
        cursor = db[collection].find()
        json_data = json.dumps(list(cursor), default=json_util.default)
        
        return json_data

    def find_element(self, db_name: str, collection: str, query: dict):

        client = self._connect()
        db = client[db_name]

        return db[collection].find_one(query, {'_id': 0})

    def add_element(self, db_name: str, collection: str, element: dict) -> None:
        
        client = self._connect()
        db = client[db_name]
        db[collection].insert_one(element)

        return

    def delete_element(self, db_name: str, collection: str, element: dict) -> None:

        client = self._connect()
        db = client[db_name]
        collection = db[collection]
        db[collection].delete_one(element)

        return

        
