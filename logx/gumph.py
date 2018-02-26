
import sys
import logging
import logging.config
import io
import yaml


from .logxintrospect import get_nicest_module_name


YAML_CONFIG_PATH = 'loggers.yaml'

DEFAULT_FORMAT = \
    '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s'


def load_yaml_config(yaml_config_path=YAML_CONFIG_PATH):
    with io.open(yaml_config_path) as f:
        yaml_config_text = f.read()

    yaml_config = yaml.load(yaml_config_text)
    logging.config.dictConfig(yaml_config)


class StdHandler(logging.Handler):
    def emit(self, record):
        msg = self.format(record)

        if record.levelno >= logging.WARNING:
            stream = sys.stderr
        else:
            stream = sys.stdout

        stream.write(msg)
        stream.write('\n')
        self.flush()


def set_basic_config():
    logging.basicConfig(level=logging.DEBUG)


def set_root_level(level='DEBUG'):
    get_logger('').setLevel(getattr(logging, level))


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    return logger


def print_diagram():
    import logging_tree
    logging_tree.printout()


class Log():
    def __init__(self):
        self.handlers = {}

    def set_level(self, level, name=None):
        handler = self.get_handler(name)
        handler.setLevel(getattr(logging, level.upper()))

    def add_std_handler(self, logger_name, level='DEBUG', top_level=True):
        if top_level:
            logger_name = logger_name.split('.')[0]

        level = level.upper()
        logging_level = getattr(logging, level)

        logger = logging.getLogger(logger_name)

        logger.setLevel(logging_level)
        h = StdHandler()
        h.setLevel(logging_level)
        logger.addHandler(h)

        return h

    def current_logger_name(self):
        name = get_nicest_module_name()
        return name

    def set_default_format(self, name=None):
        self.set_format(DEFAULT_FORMAT)

    def get_logger(self, name=None):
        name = name or self.current_logger_name()
        return logging.getLogger(name)

    def get_handler(self, name=None, top_level=True):
        name = name or self.current_logger_name()

        if top_level:
            name = name.split('.')[0]

        logger = self.get_logger(name)

        for h in logger.handlers:
            if isinstance(h, (StdHandler, logging.NullHandler)):
                return h

        raise KeyError('no logx-related handler found on this logger')

    def set_format(self, formatstring, logger_name=None, top_level=True):
        logger_name = logger_name or self.current_logger_name()

        if top_level:
            logger_name = logger_name.split('.')[0]

        try:
            handler = self.get_handler(logger_name)
        except KeyError:
            handler = None

        if not handler:
            handler = self.add_std_handler(logger_name)

        formatter = logging.Formatter(formatstring)
        handler.setFormatter(formatter)

    def set_null_handler(self, name=None, top_level=True):
        name = name or self.current_logger_name()

        if top_level:
            name = name.split('.')[0]

        logger = self.get_logger(name=name)

        logger.handlers = [
            _ for _ in logger.handlers
            if not isinstance(_, StdHandler)
        ]

        logger.addHandler(logging.NullHandler())
        print_diagram()

    def clear_null_handler(self, name=None, top_level=True):
        name = name or self.current_logger_name()

        if top_level:
            name = name.split('.')[0]

        logger = self.get_logger(name=name)

        logger.handlers = [
            _ for _ in logger.handlers
            if not isinstance(_, logging.NullHandler)
        ]

    def __getattr__(self, method, *args, **kwargs):
        if method.startswith('_'):
            raise AttributeError
        logger_name = self.current_logger_name()

        try:
            self.get_handler(logger_name)
        except KeyError:
            self.add_std_handler(logger_name)

        _logger = logging.getLogger(logger_name)
        return getattr(_logger, method)
