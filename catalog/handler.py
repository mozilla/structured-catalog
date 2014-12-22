from mozlog.structured.reader import LogHandler


class StoreResultsHandler(LogHandler):

    def __init__(self, datastore):
        self.store = datastore
        LogHandler.__init__(self)

    def suite_start(self, msg):
        # TODO extract and store relevant data
        pass

    def test_start(self, msg):
        # TODO extract and store relevant data
        pass

    def test_status(self, msg):
        # TODO extract and store relevant data
        pass

    def test_end(self, msg):
        # TODO extract and store relevant data
        pass
