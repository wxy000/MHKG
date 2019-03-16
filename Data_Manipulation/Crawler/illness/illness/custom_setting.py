jibing_settings = {
    'ITEM_PIPELINES': {
        'illness.pipelines.JibingPipeline': 300,
    }
}

neopathy_settings = {
    'ITEM_PIPELINES': {
        'illness.pipelines.NeopathyPipeline': 300,
    }
}

symptom_settings = {
    'ITEM_PIPELINES': {
        'illness.pipelines.SymptomPipeline': 300,
    }
}

inspect_settings = {
    'ITEM_PIPELINES': {
        'illness.pipelines.InspectPipeline': 300,
    }
}

drug_settings = {
    'ITEM_PIPELINES': {
        'illness.pipelines.DrugPipeline': 300,
    }
}
