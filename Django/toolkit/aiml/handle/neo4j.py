# -*- coding: utf-8 -*-
import json

from py2neo import Graph, NodeMatcher


class Find:

    # 连接数据库
    graph = Graph("http://localhost:7474", username="neo4j", password="wxy123456")

    # 根据title查询节点及其属性
    def matchNodebyTitle(self, title):
        matcher = NodeMatcher(self.graph)
        tmp = matcher.match(title=title).first()
        tmp = json.dumps(tmp, ensure_ascii=False).replace(u'\xa0', u'')
        tmp = json.loads(tmp)
        return tmp
