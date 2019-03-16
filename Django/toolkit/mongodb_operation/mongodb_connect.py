# -*- coding: utf-8 -*-

import pymongo

settings = {
    "ip": 'localhost',
    "port": 27017,
    "db_name": "mhkg"
}


class MongoDB:

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
