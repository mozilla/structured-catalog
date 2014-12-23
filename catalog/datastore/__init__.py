from .elasticsearch import ElasticSearchStore


def get_storage_backend(backend, host=None, port=None):
    store_map = {
        'elasticsearch': ElasticSearchStore,
    }

    if backend not in store_map:
        raise KeyError("Unrecognized store '{}'".format(backend))

    return store_map[backend](host=host, port=port)

