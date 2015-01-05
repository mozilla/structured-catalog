from .base import BaseQueue

mongo = None
def do_delayed_imports():
    global mongo
    import mongo 

class MongoQueue(BaseQueue):

    def __init__(self):
        BaseQueue.__init__(self)
        do_delayed_imports()

    def push(self, job):
        pass

    def get(self):
        pass

    def remove(self, msg):
        pass
