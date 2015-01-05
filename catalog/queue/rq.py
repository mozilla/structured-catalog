from .base import BaseQueue

redis = None
rq = None
def do_delayed_imports():
    global redis
    global rq
    import redis
    import rq

class RQueue(BaseQueue):

    def __init__(self):
        BaseQueue.__init__(self)
        do_delayed_imports()

    def push(self, job):
        pass

    def get(self):
        pass

    def remove(self, msg):
        pass
