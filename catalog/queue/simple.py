from catalog.queue.base import BaseQueue
from pyLibrary.debugs.logs import Log


class SimpleQueue(BaseQueue):

    def push(self, data):
        process_test_job(data)

    def get(self):
        pass

    def remove(self, job):
        pass
