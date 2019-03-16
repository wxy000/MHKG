# -*- coding: utf-8 -*-

from .mongodb_connect import MongoDB

mongo = MongoDB()
mongo.connectDB()
mydb = mongo.mydb


def collection(name):
    mycol = mydb[name]
    collist = mydb.list_collection_names()
    if name in collist:
        print("集合已存在！")
    else:
        print("创建集合！")
    return mycol


class Mongo:

    def getFenlei(self):
        result = list()
        for i in collection("fenlei").find({}, {"_id": 0}):
            result.append(i)
        return result

    def getEntity(self, jid):
        query = {'jid': jid}
        result = list()
        for i in collection("node").find(query, {"_id": 0}):
            result.append(i)
        return result


# Mongo().getSonFenlei('jibing_1_1')
