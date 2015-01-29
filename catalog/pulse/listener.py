import json
import sys
import traceback

from mozillapulse.consumers import NormalizedBuildConsumer
from mozlog.structured import structuredlog

from .. import utils
from ..config import settings
from pyLibrary.dot import unwrap
from ..queue import all_queues

logger = None
work_queues = []

def on_test_event(data, message):
    data = data['payload']
    build_name = "{}-{} {}".format(data['platform'], data['buildtype'], data['test'])

    def skip(reason):
        message.ack()
        logger.debug("skipping a {} job because: {}".format(build_name, reason))

    if 'blobber_files' not in data:
        return skip("'blobber_files' is not set")

    if data['tree'] in ('try',):
        return skip("job was run on an unsupported tree")

    if not utils.get_structured_log(data['blobber_files']):
        return skip("no structured log was detected in 'blobber_files'")

    # don't ack the message if an interrupt was received before message could
    # be placed on all queues
    try:
        logger.info("adding {} job to the work queues".format(build_name))
        for q in work_queues:
            q.push(data)
    except KeyboardInterrupt:
        raise
    except:
        message.ack()
        raise
    message.ack()

def listen(pulse_args):
    global logger
    global work_queues
    logger = structuredlog.get_default_logger()

    sanitized_args = pulse_args.copy()
    if 'password' in sanitized_args:
        sanitized_args['password'] = 'hunter1'
    logger.info("Starting pulse listener with args: \n{}".format(json.dumps(sanitized_args, indent=2)))
    logger.info("Placing jobs on the following queues: {}".format(', '.join(settings['work_queues'])))
    work_queues = [all_queues[q]() for q in settings['work_queues']]

    consumer = NormalizedBuildConsumer(callback=on_test_event, **unwrap(pulse_args))
    while True:
        try:
            consumer.listen()
        except IOError:
            pass
        except KeyboardInterrupt:
            logger.warning("Received SIGINT, exiting")
            sys.exit(1)
        except:
            logger.error(traceback.format_exc())
