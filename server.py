from pymongo import MongoClient
import mongo_url as url

client = MongoClient(host=url.url, port=27017)
db = client['crypto_db']
collection = db['user_info']

def GetUserInfo(id):
    return collection.find_one({"id":id})

def UpdateKeyData(id,data):
    collection.update_one({"id":id},{"$set":{"private_key":data}})

def InsertInfo(data):
    collection.insert_one(data)

def GetFileInfo(name,id):
    user = GetUserInfo(id)
    for file in user['Files']:
        if file.get('filename') == name:
            return file['file_list']

def UpdateFileData(id,data):
    if GetFileInfo(data.get('filename'),id) == None:
        collection.update_one({"id":id},{"$push":{"Files":data}})






