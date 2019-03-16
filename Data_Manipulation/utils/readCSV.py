# -*- coding: utf-8 -*-

import csv


# 读取csv的二维数组，第一行是列名
def readCSV(filename):
    csvlist = []
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            csvlist.append(row)
    return csvlist


# 读取csv列名对应列，不包括列名
def readCSVByColumn(filename, columnname):
    csvlist = []
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        # 表示columnname在第几列
        p = -1
        # 表示行号，0代表第一行的列名
        i = 0
        # 表示递增到columnname的一个临时变量
        j = 0
        for row in reader:
            if i == 0:
                for c in row:
                    if c == columnname:
                        p = j
                    j += 1
            else:
                csvlist.append(row[p])
            i += 1
            if p == -1:
                break
    return csvlist
