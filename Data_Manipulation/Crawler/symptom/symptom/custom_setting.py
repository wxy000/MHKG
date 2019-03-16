zhengzhuang_settings = {
    'ITEM_PIPELINES': {
        'symptom.pipelines.ZhengzhuangPipeline': 300,
    }
}

zhengzhuang_symptom_settings = {
    'ITEM_PIPELINES': {
        'symptom.pipelines.ZhengzhuangSymptomPipeline': 300,
    }
}

zhengzhuang_inspect_settings = {
    'ITEM_PIPELINES': {
        'symptom.pipelines.ZhengzhuangInspectPipeline': 300,
    }
}

zhengzhuang_drug_settings = {
    'ITEM_PIPELINES': {
        'symptom.pipelines.ZhengzhuangDrugPipeline': 300,
    }
}
