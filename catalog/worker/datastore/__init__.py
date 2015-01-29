from .elasticsearch import ElasticSearchStore

store_map = {
    'elasticsearch': ElasticSearchStore,
}

def get_storage_backend(settings):
    try:
        store_map[settings.type](settings)
    except Exception, e:
        raise KeyError("Unrecognized store '{}'".format(settings.type))


