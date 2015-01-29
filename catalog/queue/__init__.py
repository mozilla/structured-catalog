from catalog.queue.simple import SimpleQueue
from sqs import SQSQueue
from rq import RQueue
from mongo import MongoQueue

all_queues = {
    'sqs': SQSQueue,
    'rq': RQueue,
    'mongo': MongoQueue,
    'simple': SimpleQueue
}
