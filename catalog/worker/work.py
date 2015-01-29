import mozfile
import requests

from .. import config
from .. import utils
from catalog.worker.unittest_logs_to_es import process_unittest
from .datastore import get_storage_backend
from pyLibrary.debugs.logs import Log


settings = config.settings
logger = None


def process_test_job(data):
    global logger
    logger = logger or utils.get_logger(name='catalog-worker')

    build_name = "{}-{} {}".format(data['platform'], data['buildtype'], data['test'])
    logger.info("now processing a '{}' job".format(build_name))

    log_url = utils.get_structured_log(data['blobber_files'])
    log_path = _download_log(log_url)

    try:
        store = get_storage_backend(config.settings.datastore)

        # TODO commit metadata about the test run
        with open(log_path, 'r') as log:
            process_unittest(log_url, data, log, store)
    except Exception, e:
        Log.error("Problem with hanlder", e)
    finally:
        mozfile.remove(log_path)

def _download_log(url):
    r = requests.get(url, stream=True)
    if r.status_code == 401:
        if hasattr(config, 'auth'):
            auth = (config.auth['user'], config.auth['password'])
            r = requests.get(url, stream=True, auth=auth)
        else:
            logger.error("The url '{}' requires authentication!".format(url))
    r.raise_for_status()

    with mozfile.NamedTemporaryFile(prefix='structured-catalog', delete=False) as tf:
        for chunk in r.iter_content(1024):
            tf.write(chunk)
        path = tf.name
    return path


if __name__=="__main__":
    from redis import Redis
    from rq import SimpleWorker, Queue

    queue = Queue(connection=Redis())
    queue.enqueue(my_long_running_job)
    worker = SimpleWorker([queue])
    worker.work(burst=True)  # Runs enqueued job
