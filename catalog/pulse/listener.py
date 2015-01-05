import json
import traceback

from mozillapulse.consumers import NormalizedBuildConsumer
from mozlog.structured import commandline

from ..config import settings
from ..queue import all_queues

logger = None
expires = 60 * 60 * 24 * 30 # 30 days
work_queues = [all_queues[q]() for q in settings['work_queues']]

def on_test_event(data, message):
    message.ack()

    data = data['payload']
    build_name = "{}-{} {}".format(data['platform'], data['buildtype'], data['test'])

    if 'blobber_files' not in data:
        logger.debug("skipping a {} job, because 'blobber_files' is not set".format(build_name))
        return

    if data['tree'] in ('try',):
        logger.debug("skipping a {} job, because it was run on an unsupported tree".format(build_name))
        return

    for name, url in data['blobber_files'].iteritems():
        if name in settings['structured_log_names']:
            break
    else:
        logger.debug("skipping a {} job, because no structured log was detected in 'blobber_files'".format(build_name))
        return

    logger.debug("adding {} job to the work queues".format(build_name))
    for q in work_queues:
        q.push(data)

def listen(pulse_args):
    global logger
    logger = commandline.get_default_logger()
    consumer = NormalizedBuildConsumer(callback=on_test_event, **pulse_args)

    while True:
        try:
            consumer.listen()
        except IOError:
            pass
        except KeyboardInterrupt:
            raise
        except:
            traceback.print_exc()
