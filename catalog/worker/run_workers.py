from threading import Thread
from multiprocessing import Process
import argparse
import subprocess
import sys
import time

from ..queue import all_queues
from .worker import process_test_job

def busy_wait_worker(qname):
    """
    Worker that polls the queue indefinitely.
    """
    q = all_queues[qname]()
    while True:
        data = q.get()
        if not data:
            time.sleep(10)
        else:
            process_test_job(data)

def burst_worker(qname):
    """
    Worker that exits once the queue is Empty.
    """
    q = all_queues[qname]()
    data = q.get(q)
    while data:
        process_test_job(data)
        data = q.get()

def rq_worker(qname):
    """
    Spawns an rqworker in a subprocess.
    """
    subprocess.check_call(['rqworker'])

def cli(args=sys.argv[1:]):
    worker_map = {
        'rq': rq_worker,
        'sqs': busy_wait_worker,
        'mongo': burst_worker,
    }

    parser = argparse.ArgumentParser()
    parser.add_argument('queue',
                        choices=worker_map.keys(),
                        help='The work queue the workers should grab jobs from.')
    parser.add_argument('-j',
                        dest='num_workers',
                        type=int,
                        default=1,
                        help='The number of worker processes to spawn.')
    args = vars(parser.parse_args(args))

    qname = args['queue']
    process_class = Process
    if qname == 'rq':
        process_class = Thread

    for _ in args['num_workers']:
        worker = process_class(target=worker_map[qname], args=(qname,))
        worker.start()


if __name__ == '__main__':
    sys.exit(cli())
