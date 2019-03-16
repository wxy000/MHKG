# -*- coding: utf-8 -*-
import os

from jsonFormat import jsonFormat

local_url = os.path.abspath(os.path.join(os.getcwd(), "../data"))

jf = jsonFormat()
jf.format('检查', 'jiancha_', os.path.join(local_url, 'jiancha.json'), os.path.join(local_url, 'jiancha_classify.json'), os.path.join(local_url, 'jiancha_node.json'))
