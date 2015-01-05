from .base import BaseStore

elasticsearch = None

class ElasticSearchStore(BaseStore):

    @classmethod
    def do_delayed_imports(cls):
        global elasticsearch
        import elasticsearch

    def connect(self, host='localhost', port=9200):
        node = { 'host': host, 'port': port }
        #self.es = elasticsearch.Elasticsearch([node])

    def commit(self, *args, **kwargs):
        #self.es.create(*args, **kwargs)
        pass
