# -*- coding: utf-8 -*-
import json

import pymongo

settings = {
    "ip": 'localhost',
    "port": 27017,
    "db_name": "chatlog"
}


class mongo_chatlog:
    def __init__(self):
        try:
            self.myclient = pymongo.MongoClient(settings["ip"], settings["port"])
        except Exception as e:
            print(e)
        self.mydb = self.myclient[settings['db_name']]

    def connectDB(self):
        dblist = self.myclient.list_database_names()
        if settings['db_name'] in dblist:
            print("数据库已存在！")
        else:
            print("创建数据库！")

    def collection(self, name):
        collist = self.mydb.list_collection_names()
        count = 0
        mycol = self.mydb[name[0]]
        for i in name:
            if i in collist:
                count += 1
                mycol = self.mydb[i]
        return mycol

    def insertChatLog(self, mineId, toId, message):
        msg = {'username': message['username'], 'id': message['id'], 'avatar': message['avatar'],
               'timestamp': message['timestamp'], 'content': message['content']}
        x = self.collection(["chatlog_" + str(mineId) + "_" + str(toId), "chatlog_" + str(toId) + "_" + str(mineId)]).insert_one(msg)
        if x is not None:
            print("插入成功")
            return True
        else:
            print("插入失败，未知错误")
            return False

    # def getNodeByEmail(self, key):
    #     x = self.collection(settings['collection_name']).find({'doctoremail': key})
    #     return [xx for xx in x]
    #
    # def uploadById(self, key, infoDict):
    #     x = self.collection(settings['collection_name']).update_many({'doctorId': key}, {'$set': infoDict})
    #     return x.modified_count
    #
    # def login(self, doctorDict):
    #     x = self.collection(settings['collection_name']).find_one(doctorDict, {'_id': 0})
    #     return x
    #
    def getChatLogByQuery(self, id1, id2):
        x = self.collection(["chatlog_" + str(id1) + "_" + str(id2), "chatlog_" + str(id2) + "_" + str(id1)]).find({}, {'_id': 0})
        return [xx for xx in x]
    #
    # def deleteById(self, doctorId):
    #     x = self.collection(settings['collection_name']).delete_many({'doctorId': doctorId})
    #     return x.deleted_count


# t = mongo()
# print(t.login({'doctorId': 'YS19032300', 'doctorpassword': '000000'}))
