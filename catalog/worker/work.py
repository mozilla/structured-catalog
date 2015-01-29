from mozlog.structured import reader
import mozfile
import requests

from .. import config
from .. import utils
from catalog.worker.unittest_logs_to_es import StoreResultsHandler
from .datastore import get_storage_backend

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
        store = get_storage_backend(settings.datastore)

        # TODO commit metadata about the test run

        handler = StoreResultsHandler(data, store)
        with open(log_path, 'r') as log:
            iterator = reader.read(log)
            reader.handle_log(iterator, handler)
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
