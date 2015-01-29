import argparse
import os
import sys

from mozlog.structured import commandline

from catalog import config
from catalog.pulse.listener import listen

def cli(args=sys.argv[1:]):
    parser = argparse.ArgumentParser()
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
                    dest='database_backend',
                    choices=['elasticsearch'],
                    default='elasticsearch',
                    help='The type of database to use')
    pulse = parser.add_argument_group('Pulse')
    pulse.add_argument('--topic',
                       dest='pulse_topic',
                       default='unittest.#',
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
    logger = commandline.setup_logging("catalog-listener", args)

    config.read_runtime_config(os.path.expanduser('~/.catalogrc'))

    pulse_args = config.pulse
    pulse_args.update({k[len('pulse_'):]: v for k, v in args.items() if k.startswith('pulse') if v is not None})

    listen(pulse_args)


if __name__ == '__main__':
    sys.exit(cli())
