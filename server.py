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

def DeleteFileData(id,name):
    collection.update_one({"id":id},{"$pull":{"Files":{"filename" : name}}})

def UpdateFileData(id,data):
    collection.update_one({"id":id},{"$push":{"Files":data}})

def GetAllFileInfo(id):
    user = GetUserInfo(id)
    return user['Files']






