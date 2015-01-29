import argparse
import os
import sys

from mozlog.structured import commandline

from catalog import config
from catalog.pulse.listener import listen
from pyLibrary.debugs import constants
from pyLibrary.debugs.logs import Log
from pyLibrary.debugs.mozlog import use_mozlog
from pyLibrary.dot import set_default


def cli(args=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('--settings',
        dest='settings',
        required=True,
        default="./config/dev-debug.json",
        help='The config settings file'
    )

    # setup logging args
    commandline.log_formatters = { k: v for k, v in commandline.log_formatters.iteritems() if k in ('raw', 'mach') }
    commandline.add_logging_group(parser)

    args = vars(parser.parse_args(args))

    global logger
    logger = commandline.setup_logging("catalog-listener", args)
    use_mozlog()
    config.read_runtime_config(args["settings"])
    constants.set(config.settings.constants)

    listen(config.settings.pulse)


if __name__ == '__main__':
    sys.exit(cli())
