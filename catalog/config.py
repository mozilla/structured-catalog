
from ConfigParser import ConfigParser
from pyLibrary.dot import wrap
import os


settings = wrap({
    'datastore': 'elasticsearch',
    'structure d_log_names': ['raw_structured_logs.log', 'wpt_structured_full.log', 'mn_structured_full.log', '*_raw.log'],
    'work_queues': ['rq', 'mongo'],
    "pulse":None,
    "database":None
})
# globals()['pulse'] = {}
# globals()['database'] = {}

def read_runtime_config(config_path):
    if not os.path.isfile(config_path):
        raise OSError("Invalid file path '{}'!".format(config_path))

    cp = ConfigParser()
    cp.read(config_path)
    for section in cp.sections():
        if section == 'settings':
            items = dict([(k.upper(), v) for k, v in cp.items(section)])
        else:
            items = dict(cp.items(section))

        if section in settings:
            settings[section].update(items)
        else:
            settings[section] = items

        for k, v in settings[section].iteritems():
            try:
                settings[section][k] = int(v)
            except:
                pass
