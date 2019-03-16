# -*- coding: utf-8 -*-
import copy

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


class MongoLabel:
    stackTemp = list()
    stack = list()

    def getJid(self, nid, name):
        nid = int(nid)
        query = {'nid': nid, 'name': name}
        result = list()
        for i in collection("node").find(query, {"_id": 0, 'jid': 1}):
            result.append(i['jid'])
        return result

    def getLabel(self, jid):
        fenlei = list()
        for i in collection("fenlei").find({}, {"_id": 0}):
            fenlei.append(i)
        return self.getL(jid, fenlei)

    # def getL(self, jid, fenlei):
    #     for element in fenlei:
    #         self.stackTemp.append(element['name'])
    #         if element['id'] == jid:
    #             # print(self.stackTemp)
    #             self.stack = copy.deepcopy(self.stackTemp)
    #             return self.stackTemp
    #         else:
    #             if len(element['children']) <= 0:
    #                 self.stackTemp.pop()
    #             else:
    #                 self.getL(jid, element['children'])
    #                 self.stackTemp.pop()

    def getL(self, jid, fenlei):
        for i in fenlei:
            if i['id'] == jid:
                return [i['name']]
            else:
                for j in i['children']:
                    if j['id'] == jid:
                        return [i['name'], j['name']]
                    else:
                        for k in j['children']:
                            if k['id'] == jid:
                                return [i['name'], j['name'], k['name']]


# t = MongoLabel()
# print(t.getJid(1, '肝炎双重感染'))
# print(t.getLabel('drug_1_2'))
