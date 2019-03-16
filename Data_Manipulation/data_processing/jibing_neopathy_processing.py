# -*- coding: utf-8 -*-
import json
import os

from neo4j_crud import Find


def main():
    # 加载neo4j查询类
    neo = Find()
    # 数据文件位置
    local_url = os.path.abspath(os.path.join(os.getcwd(), "../data"))

    # 写入文件头
    with open(os.path.join(local_url, 'jibing_new_node.csv'), 'w') as f:
        f.write("title,lable" + '\n')
    with open(os.path.join(local_url, 'jibing_neopathy_relation.csv'), 'w') as f:
        f.write("entity1,relation,entity2" + '\n')
    with open(os.path.join(local_url, 'jibing_neopathy_relation_newnode.csv'), 'w') as f:
        f.write("entity,relation,NewNode" + '\n')

    # 读取entityRelation.json并将数据追加到另外三个文件中
    with open(os.path.join(local_url, 'jibing_neopathy_corrected.json'), 'r') as fer:
        with open(os.path.join(local_url, 'jibing_new_node.csv'), 'a') as fnn:
            with open(os.path.join(local_url, 'jibing_neopathy_relation.csv'), 'a') as fwr:
                with open(os.path.join(local_url, 'jibing_neopathy_relation_newnode.csv'), 'a') as fwrn:
                    newNodeList = list()
                    # 存储查询过的实体，避免重复查询，浪费时间
                    entitylist1 = dict()
                    entitylist2 = dict()

                    for line in fer:
                        entityRelationJson = json.loads(line)
                        # 实体1
                        entity1 = entityRelationJson['entity1']
                        # 实体2
                        entity2 = entityRelationJson['entity2']
                        # 关系
                        entityRelation = entityRelationJson['relation']
                        print(entity1 + "=======" + entity2)

                        if entity1 in entitylist1.keys():
                            find_entity1 = entitylist1[entity1]
                        else:
                            # 查询实体1
                            find_entity1 = neo.matchNodebyTitle('疾病', entity1)
                            entitylist1[entity1] = find_entity1
                        if entity2 in entitylist2.keys():
                            find_entity2 = entitylist2[entity2]
                        else:
                            # 查询实体2
                            find_entity2 = neo.matchNodebyTitle('疾病', entity2)
                            entitylist2[entity2] = find_entity2

                        # 如果实体1不存在于数据库中，则执行下一个循环
                        if find_entity1 is None:
                            continue
                        # 如果entity2既不在实体列表中，又不在NewNode中，则新建一个节点，该节点的lable为newNode，然后添加关系
                        if find_entity2 is None:
                            if entity2 not in newNodeList:
                                fnn.write(entity2 + "," + "newNode" + '\n')
                                newNodeList.append(entity2)
                            fwrn.write(entity1 + "," + entityRelation + "," + entity2 + '\n')
                        # 如果entity2在实体列表中，直接连关系即可
                        else:
                            fwr.write(entity1 + "," + entityRelation + "," + entity2 + '\n')


if __name__ == "__main__":
    main()
