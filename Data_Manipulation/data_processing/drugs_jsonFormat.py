# -*- coding: utf-8 -*-
import os

from jsonFormat import jsonFormat

local_url = os.path.abspath(os.path.join(os.getcwd(), "../data"))

jf = jsonFormat()
jf.format('药品', 'drug_', os.path.join(local_url, 'drugs.json'), os.path.join(local_url, 'drugs_classify.json'), os.path.join(local_url, 'drugs_node.json'))
