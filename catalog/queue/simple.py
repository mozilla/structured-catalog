from catalog.queue.mongo import MongoQueue
from catalog.queue.base import BaseQueue
from catalog.worker import process_test_job
from pyLibrary.dot import wrap


class SimpleQueue(BaseQueue):

    def push(self, data):
        data = wrap(data)
        data.blobber_files = {k.replace(MongoQueue.dot_encoding, '.'): v for k,v in data.blobber_files.items()}

        process_test_job(data)

    def get(self):
        pass

    def remove(self, job):
        pass
