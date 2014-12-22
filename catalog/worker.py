from threading import Thread
from Queue import Queue
import tempfile
import traceback

from mozlog.structured import (
    reader,
    structuredlog,
)
import mozfile
import requests

from . import config
from .datastore import get_storage_backend
from .handler import StoreResultsHandler

settings = config.settings
test_queue = Queue(maxsize=settings['max_queue_size'])
logger = None

class Worker(Thread):
    def __init__(self):
        Thread.__init__(self, target=self.do_work)
        self.daemon = True

        global logger
        logger = logger or structuredlog.get_default_logger()

    def do_work(self):
        while True:
            data = test_queue.get() # blocking
            try:
                self.process_test_job(data)
            except:
                # keep on truckin' on
                logger.error("encountered an exception:\n{}.".format(traceback.format_exc()))
            test_queue.task_done()

    def process_test_job(self, data):
        friendly_name = "{}-{} {}".format(data['platform'], data['buildtype'], data['test'])
        logger.debug("now processing a '{}' job".format(friendly_name))

        log_url = None
        for name, url in data['blobber_files'].iteritems():
            if name in settings['structured_log_names']:
                log_url = url
                break
        log_path = self._download_log(log_url)

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

    def _download_log(self, url):
        r = requests.get(url, stream=True)
        if r.status_code == 401:
            if hasattr(config, 'auth'):
                auth = (config.auth['user'], config.auth['password'])
                r = requests.get(url, stream=True, auth=auth)
            else:
                logger.error("The url '{}' requires authentication!".format(url))
        r.raise_for_status()

        tf, path = tempfile.mkstemp(prefix='structured-catalog')
        for chunk in r.iter_content(1024):
            tf.write(chunk)
        tf.close()
        return path

