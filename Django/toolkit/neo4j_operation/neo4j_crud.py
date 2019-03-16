# -*- coding: utf-8 -*-
import json
import re

from .neo4j_connect import Neo4j

neo = Neo4j()
neo.connectDB()
graph = neo.graph


class Find:
    # 根据id查询节点及其属性
    def matchNodebyId(self, id):
        # matcher = NodeMatcher(graph)
        # result = matcher.match(nodeName, title=value).first()
        result = graph.run('match (n) where id(n)=' + str(id) + ' return n')
        tmp = ''
        if result != '' and result is not None:
            tmp = result.data()[0]['n']
            tmp['label'] = self.matchNodeLabel(id)
            tmp['id'] = str(id)
        # 将取到的数据转为json
        tmp = json.dumps(tmp, ensure_ascii=False).replace(u'\xa0', u'')
        tmp = json.loads(tmp)
        # print(tmp)
        return tmp

    # 根据title查询节点及其关系
    def matchNodeRelationbyTitle(self, nodeName, value):
        result = list()
        if nodeName == '*':
            p = graph.run('match (n)-[]-(x) where n.title="' + value + '" return n, x, id(n) as nid, id(x) as xid')
            links_data = graph.run('MATCH (n)-[r]-() where n.title="' + value + '" RETURN r').data()
        else:
            p = graph.run('match (n:' + nodeName + ')-[]-(x) where n.title="' + value + '" return n, x, id(n) as '
                                                                                        'nid, id(x) as xid')
            links_data = graph.run('MATCH (n:' + nodeName + ')-[r]-() where n.title="' + value + '" RETURN r').data()
        links = self.get_links(links_data)
        # print(p.data())
        for i in p:
            # i.data()['n']['label'] = '疾病'
            # print(i['x']['title'])
            # print(i['nid'])
            i['n']['label'] = self.matchNodeLabel(i['nid'])
            i['x']['label'] = self.matchNodeLabel(i['xid'])
            i['n']['id'] = i['nid']
            i['x']['id'] = i['xid']
            i = json.dumps(i, ensure_ascii=False).replace(u'\xa0', u'')
            i = json.loads(i)
            # print(i)
            result.append(i[0])
            result.append(i[1])
        # print([result])
        return result, links

    # 根据id查询节点对应的label（标签）
    def matchNodeLabel(self, id):
        p = graph.run('MATCH (n) where id(n)=' + str(id) + ' RETURN distinct labels(n)')
        label = ''
        for i in p:
            i = json.dumps(i, ensure_ascii=False).replace(u'\xa0', u'')
            i = json.loads(i)
            label = i
        # print(label[0][0])
        return label[0][0]

    # 模糊查询
    def likeMatchNodeByTitle(self, value):
        p = graph.run('match (n) where n.title =~".*' + value + '.*" return n, id(n) as id')
        node = list()
        for i in p:
            i['n']['id'] = i['id']
            i = json.dumps(i, ensure_ascii=False).replace(u'\xa0', u'')
            i = json.loads(i)
            if i not in node:
                node.append(i)
        # print(node)
        return node

    # 查询所有关系
    def matchAllRelation(self):
        p = graph.run('match ()-[r]-() return distinct type(r)')
        relations = list()
        for i in p:
            i = json.dumps(i, ensure_ascii=False).replace(u'\xa0', u'')
            i = json.loads(i)
            relations.append(i[0])
        # print(relations)
        return relations

    # 查询关系
    def matchRelationByNode(self, node1, node2, r):
        nodes = list()
        ids = set()
        dict = {}
        links_data = ''
        if node1 == 'undefined' and node2 != 'undefined':
            links_data = graph.run('match (n)-[r:' + r + ']-(x) where id(x)=' + str(node2) + ' return r').data()
        elif node2 == 'undefined' and node1 != 'undefined':
            links_data = graph.run('match (n)-[r:' + r + ']-(x) where id(n)=' + str(node1) + ' return r').data()
        elif node1 != 'undefined' and node2 != 'undefined':
            if r == '0':
                links_data = graph.run(
                    'START a=node(' + str(node1) + '), b=node(' + str(node2) + ') MATCH n=shortestPath((a)-[r*]-(b)) '
                                                                               'return r').data()
            elif r == '*':
                links_data = graph.run(
                    'START a=node(' + str(node1) + '), b=node(' + str(node2) + ') MATCH n=allshortestpaths((a)-[r*]-('
                                                                               'b)) return r').data()
        links = self.get_links(links_data)
        for link in links:
            ids.add(link['source'])
            ids.add(link['target'])
        for id in ids:
            dict['id'] = id
            dict['title'] = self.get_node(id)
            dict['label'] = self.matchNodeLabel(id)
            nodes.append(dict)
            dict = {}
        # print(nodes)
        # print(links)
        return nodes, links

    def get_links(self, links_data):
        """知识图谱关系数据获取"""
        links_data_str = str(links_data)
        links = []
        i = 1
        dict = {}
        # 正则匹配
        # print(links_data_str)
        links_str = re.sub("[\!\%\[\]\,\。\{\}\-\:\'\(\)\>\_]", " ", links_data_str)
        links_str = re.sub(r"\\u\w+", " ", links_str)
        links_str = re.sub("r", " ", links_str)
        links_str = re.sub("type", " ", links_str).split(' ')
        # print(links_str)
        for link in links_str:
            if len(link) > 0:
                if i == 1:
                    dict['source'] = link
                elif i == 2:
                    dict['name'] = link
                elif i == 3:
                    dict['target'] = link
                    links.append(dict)
                    dict = {}
                    i = 0
                i += 1
        return links

    def get_node(self, id):
        """根据id查询节点title"""
        p = graph.run('MATCH (n) WHERE id(n)=' + str(id) + ' RETURN n.title as title')
        # print(p.data()[0]['title'])
        return p.data()[0]['title']

    # 模糊查询节点
    def matchAllNode(self, value):
        result = graph.run('match (n) where n.title =~".*' + value + '.*" return n.title as title, id(n) as id')
        node = list()
        for i in result:
            i = json.dumps(i.data(), ensure_ascii=False).replace(u'\xa0', u'')
            i = json.loads(i)
            node.append(i)
            # print(i)
        # print(node)
        return node

    # 根据title查询节点
    def matchItemByTitle(self, title):
        result = graph.run('match (n) where n.title = "' + str(title) + '" return n, id(n) as id')
        node = list()
        for i in result:
            i = json.dumps(i.data(), ensure_ascii=False).replace(u'\xa0', u'')
            i = json.loads(i)
            node.append(i)
        return node

# t = Find()
# t.matchRelationByNode("肺癌", "", "肺地丝菌病")
