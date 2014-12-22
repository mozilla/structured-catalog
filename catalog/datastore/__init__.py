from abc import ABCMeta, abstractmethod

from .elasticsearch import ElasticSearchStore

class BaseStore(object):
    __metaclass__ = ABCMeta

    def __init__(self, host=None, port=None):
        self.do_delayed_imports()
        self.connect(host=host, port=port)

    @abstractmethod
    def do_delayed_imports(self):
        pass

    @abstractmethod
    def connect(self, host=None, port=None):
        pass

    @abstractmethod
    def commit(self, *args, **kwargs):
        pass


def get_storage_backend(db_type, host=None, port=None):
    store_map = {
        'elasticsearch': ElasticSearchStore,
    }

    if db_type not in store_map:
        raise KeyError("Unrecognized store '{}'".format(db_type))

    return store_map[db_type](host=host, port=port)

