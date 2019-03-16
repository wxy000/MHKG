# -*- coding: utf-8 -*-

import csv
import json


class csv2json:

    # 读csv文件
    def read_csv(self, file):
        csv_rows = []
        with open(file) as csvfile:
            reader = csv.DictReader(csvfile)
            title = reader.fieldnames
            for row in reader:
                csv_rows.extend([{title[i]: row[title[i]] for i in range(len(title))}])
            return csv_rows

    # 写json文件
    def write_json(self, data, json_file, format=None):
        with open(json_file, "w") as f:
            if format == "good":
                f.write(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False))
            else:
                f.write(json.dumps(data))


class json2csv:

    def read_json(self, filename):
        return json.loads(open(filename).read())

    def write_csv(self, data, filename):
        with open(filename, 'w') as outf:
            dw = csv.DictWriter(outf, data[0].keys(), quoting=csv.QUOTE_ALL)
            dw.writeheader()
            for row in data:
                dw.writerow(row)

    # 适用于一行一个json的情况
    def trans(self, inputfilename, outputfilename):
        jsondata = open(inputfilename, 'r')
        csvdata = open(outputfilename, 'w', newline='')
        writer = csv.writer(csvdata, delimiter=',')
        flag = True
        for line in jsondata:
            dic = json.loads(line[0:-1])
            if flag:
                # 获取属性列表
                keys = list(dic.keys())
                print(keys)
                # 将属性列表写入csv中
                writer.writerow(keys)
                flag = False
            # 读取json数据的每一行，将values数据一次一行的写入csv中
            writer.writerow(list(dic.values()))
        jsondata.close()
        csvdata.close()
