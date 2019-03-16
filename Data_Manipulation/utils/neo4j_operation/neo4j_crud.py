# -*- coding: utf-8 -*-
from py2neo import NodeMatcher

from neo4j_connect import Neo4j

neo = Neo4j()
neo.connectDB()
graph = neo.graph


class Find:
    def matchNodebyTitle(self, nodeName, value):
        matcher = NodeMatcher(graph)
        result = matcher.match(nodeName, title=value).first()
        # print(result)
        return result

    def matchId(self, nodeType, value):
        result = graph.run('match(n:' + nodeType + ') where n.title="' + value + '" return id(n) as n')
        # print(result.data()[0]['n'])
        return result.data()[0]['n']
        # with open('1.txt', 'a') as a:
        #     a.write(str(result.data()) + '\n' + value + '\n')
        # return '##'


# t = Find()
# t.matchId("疾病", '糖尿病')
