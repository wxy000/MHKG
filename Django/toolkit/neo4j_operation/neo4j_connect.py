# -*- coding: utf-8 -*-
from py2neo import Graph


class Neo4j:
    graph = None

    def __init__(self):
        print("create neo4j class ...")

    def connectDB(self):
        self.graph = Graph("http://localhost:7474", username="neo4j", password="wxy123456")
        print("connect succeed")


# test = Neo4j()
# test.connectDB()
