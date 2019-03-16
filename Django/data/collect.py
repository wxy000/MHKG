# -*- coding: utf-8 -*-

import os

from readCSV import readCSVByColumn

local_url = os.path.abspath(os.getcwd())
titles = readCSVByColumn(os.path.join(local_url, 'drugs.csv'), 'title')

with open(os.path.join(local_url, 'labeled_data.txt'), 'a') as f:
    for i in titles:
        f.write('4 ' + i + '\n')
