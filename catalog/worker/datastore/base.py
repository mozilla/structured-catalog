from abc import ABCMeta, abstractmethod
from pyLibrary.meta import use_settings


class BaseStore(object):
    __metaclass__ = ABCMeta

    @use_settings
    def __init__(self, settings):
        self.do_delayed_imports()
        self.connect()

    @abstractmethod
    def do_delayed_imports(self):
        pass

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def extend(self, records):
        """
        :param records: list of records
        :return:
        """
        pass

    @abstractmethod
    def add(self, record):
        """
        :param record: one record to add
        :return:
        """

