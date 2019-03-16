# -*- coding: utf-8 -*-
import os

from jsonFormat import jsonFormat

local_url = os.path.abspath(os.path.join(os.getcwd(), "../data"))

jf = jsonFormat()
jf.format('疾病', 'jibing_', os.path.join(local_url, 'jibing.json'), os.path.join(local_url, 'jibing_classify.json'), os.path.join(local_url, 'jibing_node.json'))
