import argparse
import sys
import time

from mozlog.structured import commandline
from requests.exceptions import HTTPError

from ..queue import all_queues
from .work import process_test_job

def busy_wait_worker(q, interval=10):
    """
    Worker that polls the queue indefinitely.
    """
    while True:
        data = q.get()
        if not data:
            time.sleep(interval)
        else:
            process_test_job(data)

def burst_worker(q):
    """
    Worker that exits once the queue is Empty.
    """
    data = q.get()
    while data:
        try:
            process_test_job(data)
        except HTTPError as e:
            if e.response.status_code == 404:
                # the structured log no longer exists
                q.remove(data)
        data = q.get()


def cli(args=sys.argv[1:]):
    worker_map = {
        'sqs': busy_wait_worker,
        'mongo': burst_worker,
    }

    parser = argparse.ArgumentParser()
    parser.add_argument('queue',
                        choices=worker_map.keys(),
                        help='The work queue the worker should grab jobs from.')

    # setup logging args
    commandline.log_formatters = { k: v for k, v in commandline.log_formatters.iteritems() if k in ('raw', 'mach') }
    commandline.add_logging_group(parser)

    args = vars(parser.parse_args(args))
    commandline.setup_logging("catalog-worker", args)

    qname = args['queue']
    q = all_queues[qname]()
    return worker_map[qname](q)


if __name__ == '__main__':
    sys.exit(cli())
