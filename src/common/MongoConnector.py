from pymongo import MongoClient
from bson.dbref import DBRef

def get_mongo_rest_ref_by_url(db,collection,URL):

    rest=db[collection].find_one({'URL':URL})
    id=rest.get('_id')
    ref = DBRef(collection=collection,database='Restaurants',id=id)
    return ref


def connect_to_my_mongo_db(DataBaseName):
    client=get_mongo_client()
    db=client[DataBaseName]
    print(f"Connected to {DataBaseName} Database...")
    return db


def get_mongo_client():

    print('Connecting to Local MongoDB server..')
    client = MongoClient('localhost', 27017)
    return client

def disconnect(client):
    client.close()