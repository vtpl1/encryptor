import argparse
import logging
import logging.config
import os
import signal
import threading
import codecs

import yaml
import zope.event
from .data_models import shutdown_event

LOGGER = logging.getLogger(__name__)


def setup_logging(default_path='logging.yaml', default_level=logging.INFO, env_key='LOG_CFG'):
    """Setup logging configuration

    """

    path = default_path
    print("Current working directory", path)
    # value = os.getenv(env_key, None)
    # if value:
    #     path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


is_shutdown = threading.Event()


def stop_handler(signal_received, frame):
    del signal_received, frame
    LOGGER.info("")
    LOGGER.info("=============================================")
    LOGGER.info("Bradcasting global shutdown from stop_handler")
    LOGGER.info("=============================================")
    zope.event.notify(shutdown_event.ShutdownEvent("KeyboardInterrupt received"))
    global is_shutdown
    is_shutdown.set()


def raise_unhandled_exeception_error():
    LOGGER.info("")
    LOGGER.info("=============================================")
    LOGGER.info("Bradcasting unhandled exception error")
    LOGGER.info("=============================================")
    zope.event.notify(shutdown_event.ShutdownEvent("Unhandled global exception"))
    global is_shutdown
    is_shutdown.set()


def init_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Encryptor')
    parser.add_argument('-i', '--input', help="Input folder to encrypt")
    # parser.add_argument('--uid', help="Input uid, e.g. admin")
    # parser.add_argument('--passwd', help="pass, e.g. admin")

    return parser


def create_session_folder():
    if os.path.exists(os.path.join(os.getcwd(), "session")):
        print("Session folder exists")
    else:
        try:
            os.makedirs(os.path.join(os.getcwd(), "session"))
            print("Session folder created")
        except OSError:
            print("Tried creating session, but directory exists")


def read(rel_path):
    here = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version():
    return read("VERSION")


def main():
    signal.signal(signal.SIGINT, stop_handler)
    signal.signal(signal.SIGTERM, stop_handler)
    # create session folder
    create_session_folder()
    setup_logging()
    LOGGER.info("=============================================")
    LOGGER.info("              Started  {} {}               ".format(__name__, get_version()))
    LOGGER.info("=============================================")
    try:
        parser = init_argparser()
        args = parser.parse_args()
        if args.input is not None:
            LOGGER.info("Input {}".format(args.input))
        global is_shutdown
        is_shutdown.set()
        while not is_shutdown.wait(10.0):
            continue
    except Exception as e:
        LOGGER.exception(e)
        # LOGGER.fatal(e)
        raise_unhandled_exeception_error()

    LOGGER.info("=============================================")
    LOGGER.info("              Shutdown complete              ")
    LOGGER.info("=============================================")
