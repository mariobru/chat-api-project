#!/usr/bin/python3

from pymongo import MongoClient
import getpass
import json
import os

#Get Password
password = getpass.getpass("Insert your AtlasMongoDB admin_1019 password: ")
connection = "mongodb+srv://mariobru:{}@chatapi-uodzv.mongodb.net/test?retryWrites=true&w=majority".format(password)

#Connect to DB
client = MongoClient(connection)
def connectCollection(database, collection):
    db = client[database]
    coll = db[collection]
    return db, coll

db, coll = connectCollection('datamad1019','chats')

with open('/home/mariobru/git_ironhack/chat-sentiment-analysis-service/input/chats.json') as f:
    chats_json = json.load(f)
coll.insert_many(chats_json)