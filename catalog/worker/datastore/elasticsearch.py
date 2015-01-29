from .base import BaseStore
from pyLibrary.env.elasticsearch import Cluster

class ElasticSearchStore(BaseStore):

    def __init__(self, settings):
        self.index = Cluster(settings).get_or_create_index(settings)

    def connect(self):
        pass

    def commit(self, *args, **kwargs):
        pass

    def commit(self):
        pass

    def do_delayed_imports(self):
        pass

    def extend(self, records):
        """
        :param records: list of records
        :return:
        """
        self.index.extend([{"value": r} for r in records])

    def add(self, record):
        """
        :param record: one record to add
        :return:
        """
        self.index.add(record)
