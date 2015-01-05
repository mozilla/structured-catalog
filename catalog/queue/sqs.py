from Queue import Queue, Empty
import json

from .base import BaseQueue

sqs = None
def do_delayed_imports():
    global sqs
    from boto import sqs

class SQSQueue(BaseQueue):
    _cache = Queue()

    def __init__(self):
        BaseQueue.__init__(self)
        do_delayed_imports()

        self.conn = sqs.connect_to_region('us-west-2')
        self.unprocessed = self.conn.create_queue('structured-catalog-unprocessed')

    def push(self, job):
        m = sqs.message.Message()
        m.set_body(json.dumps(job))
        self.unprocessed.write(m)

    def get(self):
        try:
            msg = self._cache.get(block=False)
            self.remove(msg)
            return json.loads(msg.get_body())
        except Empty:
            rs = self.unprocessed.get_messages(num_messages=10)
            if not rs:
                return

            for msg in rs:
                self._cache.put(msg)
            return self.get()

    def remove(self, msg):
        self.unprocessed.delete_message(msg)
