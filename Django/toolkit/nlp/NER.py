# -*- coding: utf-8 -*-
import paramiko

from ..neo4j_operation.neo4j_crud import Find

from ..readLabel import predict_labels


def ssh(command):
    # 创建SSH对象
    ssh = paramiko.SSHClient()
    # 允许连接不在know_hosts文件中的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接服务器
    ssh.connect(hostname='39.108.111.94', port=22, username='root', password='Iamadeveloper0..')

    # 执行命令
    stdin, stdout, stderr = ssh.exec_command(command)
    # 获取命令结果
    result = stdout.read().decode()
    error = stderr.read().decode()

    print("------start------")
    print("[connect success] | ip : %s" % '39.108.111.94')
    if error != "":
        print("error:\n%s" % error)
    else:
        print("result:\n%s" % result)
    print("------end------")

    # 关闭连接
    ssh.close()
    return result


# aa = "一个由来自全球多家科研机构的白血病专家组成的研究小组使用血液检测和机器学习技术，来预测健康" \
#      "个体是否有患急性骨髓性白血病（AML）的风险，这项研究发表在了《自然》上，有望最多提前五年对白血病" \
#      "进行预测。急性骨髓性白血病（AML）是一种进展迅速、危及生命的血液肿瘤，可以影响所有年龄段的人群。" \
#      "这项研究意味着我们可以提早发现AML的高风险人群并进行监测，同时可以寻找降低该疾病患病几率的方案。"
# ss = ssh('./MHKGssh.sh ' + aa)
# zz = list(eval(ss[21:]))
# print(type(zz[0]))
class NER:

    def preok(self, s):  # 上一个词的词性筛选

        if s == 'n' or s == 'np' or s == 'ns' or s == 'ni' or s == 'nz':
            return True
        if s == 'v' or s == 'a' or s == 'i' or s == 'j' or s == 'x' or s == 'id' or s == 'g' or s == 'u':
            return True
        if s == 't' or s == 'm' or s == 'r':
            return True
        return False

    def nowok(self, s):  # 当前词的词性筛选

        if s == 'n' or s == 'np' or s == 'ns' or s == 'ni' or s == 'nz':
            return True
        if s == 'a' or s == 'i' or s == 'j' or s == 'x' or s == 'id' or s == 'g' or s == 'v':
            return True
        if s == 't' or s == 'm' or s == 'uw':
            return True
        return False

    def temporaryok(self, s):  # 一些暂时确定是名词短语的（数据库中可以没有）
        if s == 'np' or s == 'ns' or s == 'ni' or s == 'nz':
            return True
        if s == 'j' or s == 'x' or s == 't':
            return True
        return False

    def get_explain(self, s):
        if s == '1':
            return '疾病'
        if s == '2':
            return '症状'
        if s == '3':
            return r'检查'
        if s == '4':
            return '药品'
        if s == '5':
            return '其它实体'

        if s == 'np':
            return '人物'
        if s == 'ns':
            return '地点'
        if s == 'ni':
            return '机构'
        if s == 'nz':
            return '专业名词'
        if s == 'i' or s == 'id':
            return '习语'
        if s == 'j':
            return '简称'
        if s == 'x':
            return '其它'
        if s == 't':
            return '时间日期'

        return '非实体'

    def get_detail_explain(self, s):
        if s == '1':
            return '包括全部已知疾病名称'
        if s == '2':
            return '所有症状'
        if s == '3':
            return '全部检查项目'
        if s == '4':
            return '所有类目药品'
        if s == '5':
            return '与医疗领域没有特别直接的关系，但是也是实体'

        if s == 'np':
            return '包括人名，职位'
        if s == 'ns':
            return '包括地名，区域，行政区等'
        if s == 'ni':
            return '包括机构名，会议名，期刊名等'
        if s == 'nz':
            return ' '
        if s == 'i' or s == 'id':
            return ' '
        if s == 'j':
            return ' '
        if s == 'x':
            return ' '
        if s == 't':
            return ' '

        return '非实体'

    def get_NE(self, text):
        db = Find()
        text = text.strip()
        tagList = list(eval(ssh('cd /root/MHKGssh;./MHKGssh.sh ' + text)[21:]))
        tagList.append(['===', None])
        tagList.append(['===', None])

        labels = predict_labels

        answerList = list()

        i = 0
        length = len(tagList) - 2

        l1 = list()
        for ii in tagList:
            l1.append("'" + str(ii[0]) + "'")
        # print(str(l1).replace(' ', '').replace('\\\'"\\\'', '\"'))
        syn = dict(eval(ssh('cd /root/MHKGssh;./SYNssh.sh ' + str(l1).replace(' ', '').replace('\\\'"\\\'', '\"'))[376:]))
        # print(syn['艾滋病'])
        while i < length:
            p1 = tagList[i][0]
            t1 = tagList[i][1]
            p2 = tagList[i + 1][0]
            t2 = tagList[i + 1][1]
            p3 = tagList[i + 2][0]
            t3 = tagList[i + 2][1]

            biaodian = r"!\"#$%&'()*+,-./:;<=>?@[\]^_`{" \
                       r"|}~！？｡＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏. "
            # if (p1 not in biaodian) and (p2 not in biaodian) and (p3 not in biaodian):
            #     flag = db.matchItemByTitle(p1 + p2 + p3)
            #     if (p1 + p2 + p3) in labels and len(flag) > 0 and self.preok(t1) and self.preok(t2) and self.nowok(t3):
            #         answerList.append([p1 + p2 + p3, flag[0]['id'], labels[p1 + p2 + p3]])
            #         i += 3
            #         continue
            # if (p1 not in biaodian) and (p2 not in biaodian):
            #     flag = db.matchItemByTitle(p1 + p2)
            #     if (p1 + p2) in labels and len(flag) > 0 and self.preok(t1) and self.nowok(t2):
            #         answerList.append([p1 + p2, flag[0]['id'], labels[p1 + p2]])
            #         i += 2
            #         continue
            if p1 not in biaodian:
                fl = list()
                f = list()
                for zz in list(syn.values()):
                    if p1 in zz:
                        fl.append(zz)
                for j in fl:
                    f.append(list(syn.keys())[list(syn.values()).index(j)])
                zuihou = list(set(f).intersection(set(labels)))
                if len(zuihou) > 0:
                    word = zuihou[0]
                else:
                    word = p1
                print(p1 + "---" + word)
                if word in labels:
                    flag = db.matchItemByTitle(word)
                    if len(flag) > 0 and self.nowok(t1):
                        answerList.append([p1, word, flag[0]['id'], labels[word]])
                        i += 1
                        continue
            if self.temporaryok(t1):
                answerList.append([p1, p1, '##', ''])
                i += 1
                continue
            answerList.append([p1, p1, '#', ''])
            i += 1
        return answerList


# get_NE(aa)
