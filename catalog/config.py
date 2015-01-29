from pyLibrary import jsons
from pyLibrary.dot import wrap, set_default

settings = wrap({
    'structured_log_names': ['raw_structured_logs.log', 'wpt_structured_full.log', 'mn_structured_full.log', '*_raw.log'],
    'work_queues': None,
    "pulse": None,
    "datastore": None
})

def read_runtime_config(config_path):
    file_settings = jsons.ref.get("file://"+config_path)
    globals()["settings"] = set_default(file_settings, settings)
