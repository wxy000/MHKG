# -*- coding: utf-8 -*-

import pymongo

settings = {
    "ip": 'localhost',
    "port": 27017,
    "db_name": "doctor",
    "collection_name": "pingjia"
}


class mongo_pingjia:
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

    def insert(self, infoDict):
        xx = self.collection(settings['collection_name']).insert_one(infoDict)
        if xx is not None:
            print("插入成功")
            return True
        else:
            print("插入失败，未知错误")
            return False

    def getPingjiaByQuery(self, query):
        x = self.collection(settings['collection_name']).find(query)
        return [xx for xx in x]

    # def deleteById(self, doctorId):
    #     x = self.collection(settings['collection_name']).delete_many({'doctorId': doctorId})
    #     return x.deleted_count


# t = mongo_rate()
# print(t.insertOrUploadById(1, {'rate': 10}))
