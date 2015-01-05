from mozlog.structured import (
    reader,
    structuredlog,
)
import mozfile
import requests

from .. import config
from .datastore import get_storage_backend
from .handler import StoreResultsHandler

settings = config.settings
logger = structuredlog.get_default_logger()

def process_test_job(data):
    build_name = "{}-{} {}".format(data['platform'], data['buildtype'], data['test'])
    logger.debug("now processing a '{}' job".format(build_name))

    log_url = None
    for name, url in data['blobber_files'].iteritems():
        if name in settings['structured_log_names']:
            log_url = url
            break
    log_path = _download_log(log_url)

    try:
        db_args = config.database
        store = get_storage_backend(**db_args)

        # TODO commit metadata about the test run

        handler = StoreResultsHandler(store)
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
