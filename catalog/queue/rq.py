from __future__ import absolute_import

from .base import BaseQueue
from ..worker import process_test_job

Redis = None
Connection = None
Queue = None
def do_delayed_imports():
    global Redis
    global Connection
    global Queue
    from redis import Redis
    from rq import Queue, Connection

class RQueue(BaseQueue):

    def __init__(self):
        do_delayed_imports()
        BaseQueue.__init__(self)

        with Connection(Redis()):
            self.q = Queue('catalog')

    def push(self, job):
        self.q.enqueue(process_test_job, job)

    def get(self):
        # rq delivers jobs to workers automatically, no need for polling
        pass

    def remove(self, job):
        # jobs are not kept after delivering to worker
        pass
