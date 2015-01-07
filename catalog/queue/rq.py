from .base import BaseQueue
from ..worker import process_test_job

redis = None
rq = None
def do_delayed_imports():
    global redis
    global rq
    import redis
    import rq

class RQueue(BaseQueue):

    def __init__(self):
        do_delayed_imports()
        BaseQueue.__init__(self)

        self.redis_conn = redis.Redis()
        self.queue = rq.Queue('catalog', connection=self.redis_conn)

    def push(self, job):
        self.queue.enqueue(process_test_job, job)

    def get(self):
        # rq delivers jobs to workers automatically, no need for polling
        pass

    def remove(self, job):
        # jobs are not kept after delivering to worker
        pass
