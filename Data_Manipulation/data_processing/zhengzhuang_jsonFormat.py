# -*- coding: utf-8 -*-
import os

from jsonFormat import jsonFormat

local_url = os.path.abspath(os.path.join(os.getcwd(), "../data"))

jf = jsonFormat()
jf.format('症状', 'zhengzhuang_', os.path.join(local_url, 'zhengzhuang.json'), os.path.join(local_url, 'zhengzhuang_classify.json'), os.path.join(local_url, 'zhengzhuang_node.json'))
