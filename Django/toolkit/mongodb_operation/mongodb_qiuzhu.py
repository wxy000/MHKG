# -*- coding: utf-8 -*-

import pymongo

settings = {
    "ip": 'localhost',
    "port": 27017,
    "db_name": "doctor",
    "collection_name": "qiuzhu"
}


class mongo_qiuzhu:
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
        mycol = self.mydb[name]
        collist = self.mydb.list_collection_names()
        if name in collist:
            print("集合已存在！")
        else:
            print("创建集合！")
        return mycol

    def insertQiuzhu(self, doctordict):
        x = self.collection(settings['collection_name']).insert_one(doctordict)
        if x is not None:
            print("插入成功")
            return True
        else:
            print("插入失败，未知错误")
            return False

    def getMaxId(self, id_):
        query = {'qiuzhuId': {"$regex": "^" + str(id_)}}
        x = self.collection(settings['collection_name']).find(query).sort([('qiuzhuId', -1)]).limit(1)
        return [xx for xx in x]

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
    def getQiuzhuByQuery(self, query):
        x = self.collection(settings['collection_name']).find(query)
        return [xx for xx in x]
    #
    # def deleteById(self, doctorId):
    #     x = self.collection(settings['collection_name']).delete_many({'doctorId': doctorId})
    #     return x.deleted_count


# t = mongo()
# print(t.login({'doctorId': 'YS19032300', 'doctorpassword': '000000'}))
