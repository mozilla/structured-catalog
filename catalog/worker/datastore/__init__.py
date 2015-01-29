from .elasticsearch import ElasticSearchStore
from pyLibrary.debugs.logs import Log

store_map = {
    'elasticsearch': ElasticSearchStore,
}

def get_storage_backend(settings):
    try:
        return store_map[settings.type](settings)
    except Exception, e:
        Log.error("Unrecognized store '{{type}}'", {"type":settings.type}, e)


