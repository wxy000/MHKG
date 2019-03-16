# -*- coding: utf-8 -*-
import json
import codecs
import os

from neo4j_crud import Find


class jsonFormat:
    """
        只考虑到第一列一样的情况
    """
    def format(self, nodeType, preId, inputFile, outputFile1, outputFile2):
        if os.path.exists(outputFile1):
            os.remove(outputFile1)
        if os.path.exists(outputFile2):
            os.remove(outputFile2)
        # 判断是否已存在
        cf = set()
        nodes = list()
        w2 = codecs.open(outputFile2, 'w', encoding='utf-8')
        ll = list()
        with open(inputFile, 'r') as f:
            hangNum = 0
            for line in f.readlines():
                resultJson = json.loads(line)
                classify = resultJson['分类']
                classify = classify.split('##')

                son = dict()
                ss = ''
                for j in classify[:-1]:
                    ss += j
                son['jid'] = ss
                son['name'] = classify[-1]

                classify.pop()

                # 前一个词，用于定位
                preWord = ''
                # 去重
                word = ''
                # 记录层数(可能列与列之间会有重复)
                num = 0
                for i in classify:
                    word += i
                    if word not in cf:

                        item = dict()
                        item['id'] = preId + str(hangNum) + '_' + str(num)
                        item['name'] = i
                        item['parent'] = preWord
                        item['children'] = list()

                        node = dict()
                        node['id'] = item['id']
                        node['name'] = word
                        nodes.append(node)

                        try:
                            with open(outputFile1, 'r') as rr:
                                read = json.load(rr)
                                # read['children'].append(item)
                                # print(preWord)
                                self.walk(read, preWord, num, item)
                                with codecs.open(outputFile1, 'w', encoding='utf-8') as w0:
                                    json.dump(read, w0, indent=4, ensure_ascii=False)
                        except IOError:
                            with codecs.open(outputFile1, 'w', encoding='utf-8') as ww:
                                json.dump(item, ww, indent=4, ensure_ascii=False)

                        cf.add(word)
                    num += 1
                    preWord = i
                hangNum += 1
                for n in nodes:
                    if n['name'] == son['jid']:
                        son['jid'] = n['id']
                        nid = Find().matchId(nodeType, son['name'])
                        son['nid'] = nid
                        # json.dump(son, w2, indent=4, ensure_ascii=False)
                        ll.append(son)
            json.dump(ll, w2, indent=4, ensure_ascii=False)

    def walk(self, tree, preWord, num, item):
        if isinstance(tree, dict):
            if num == 1:
                if tree['name'] == preWord:
                    tree['children'].append(item)
            else:
                for i in tree['children']:
                    self.walk(i, preWord, num - 1, item)


# t = jsonFormat()
# t.format()
