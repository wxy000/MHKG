# -*- coding: utf-8 -*-
import csv

predict_labels = {}  # 预加载实体到标注的映射字典
with open('/root/MHKG/Django/data/labeled_data.txt', 'r', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter=' ')
    for row in reader:
        name = str(row[1])
        if len(row) > 2:
            for i in range(2, len(row)):
                name += ' ' + row[i]
        predict_labels[name] = str(row[0])
