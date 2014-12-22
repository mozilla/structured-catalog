from multiprocessing import cpu_count
from Queue import Full
import argparse
import os
import sys
import time
import traceback

from mozillapulse import NormalizedBuildConsumer
from mozlog.structured import commandline

from . import config
from .worker import (
    Worker,
    test_queue
)

logger = None

def on_test_event(data, message):
    message.ack()

    data = data['payload']
    friendly_name = "{}-{} {}".format(data['platform'], data['buildtype'], data['test'])

    if 'blobber_files' not in data:
        logger.debug("skipping a {} job, because 'blobber_files' is not set".format(friendly_name))
        return

    if 'l10n' in data['tags']:
        logger.debug("skipping a {} job, because 'l10n' in tags".format(friendly_name))
        return

    for name, url in data['blobber_files'].iteritems():
        if name in config.general['structured_log_names']:
            break
    else:
        logger.debug("skipping a {} job, because no structured log was detected in 'blobber_files'".format(friendly_name))
        return

    try:
        logger.debug("adding a {} job to the queue".format(friendly_name))
        test_queue.put(data, block=False)
    except Full:
        # TODO handle overflow better, for now data is lost forever
        logger.warning("queue is full, lost a {} job".format(friendly_name))

def listen(pulse_args):
    consumer = NormalizedBuildConsumer(callback=on_test_event, **pulse_args)

    try:
        while True:
            try:
                consumer.listen()
            except IOError:
                pass
            except KeyboardInterrupt:
                raise
            except:
                traceback.print_exc()
    except KeyboardInterrupt:
        logger.info("Waiting for threads to finish processing {} jobs, press Ctrl-C again to exit now...".format(test_queue.unfinished_tasks))
        try:
            # do this instead of Queue.join() so KeyboardInterrupts get caught
            while test_queue.unfinished_tasks:
                time.sleep(1)
        except KeyboardInterrupt:
            sys.exit(1)

def run(args=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('-j', '--num-threads',
                        dest='num_threads',
                        default=cpu_count(),
                        help='Number of worker threads to spawn')
    db = parser.add_argument_group('Database')
    db.add_argument('--db-host',
                    dest='database_host',
                    default=None,
                    help='The machine hosting the database')
    db.add_argument('--db-port',
                    dest='database_port',
                    default=None,
                    help='The port the database is running behind')
    db.add_argument('--db-type',
                    dest='database_type',
                    choices=['elasticsearch'],
                    default='elasticsearch',
                    help='The type of database to use')
    pulse = parser.add_argument_group('Pulse')
    pulse.add_argument('--topic',
                       dest='pulse_topic',
                       help='The pulse topic to listen on')
    pulse.add_argument('--durable',
                       dest='pulse_durable',
                       action='store_true',
                       help='If specified, create a durable pulse queue')
    pulse.add_argument('--user',
                       dest='pulse_user',
                       help='Pulse user to register the queue to')
    pulse.add_argument('--password',
                       dest='pulse_password',
                       help='The pulse user\'s password')

    # setup logging args
    commandline.log_formatters = { k: v for k, v in commandline.log_formatters.iteritems() if k in ('raw', 'mach') }
    commandline.add_logging_group(parser)

    args = vars(parser.parse_args(args))

    global logger
    logger = commandline.setup_logging("structured-catalog", args)

    config.read_runtime_config(os.path.expanduser('~/.catalogrc'))

    pulse_args = config.pulse
    pulse_args.update({k[len('pulse_'):]: v for k, v in args.items() if k.startswith('pulse') if v is not None})

    db_args = config.database
    db_args.update({k[len('database_'):]: v for k, v in args.items() if k.startswith('database') if v is not None})

    # spawn the workers
    for _ in range(args.num_threads):
        worker = Worker()
        worker.start()

    listen(pulse_args)

if __name__ == '__main__':
    sys.exit(run())
