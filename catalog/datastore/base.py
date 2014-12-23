from abc import ABCMeta, abstractmethod

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
