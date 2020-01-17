from logx import log, print_diagram
import json
from datetime import datetime


def load_config(path):
    import io
    import os
    import yaml
    import logging

    if path and os.path.exists(path):
        with io.open(path) as f:
            conf = f.read()
        logging.config.dictConfig(yaml.load(conf))


def m(caplog):
    return caplog.records[-1].message


def test_plain_output(caplog, capsys):
    logger_name = log.current_logger_name()
    assert logger_name == "tests.test_logx"
    FIRST_MESSAGE = "first message"
    log.info(FIRST_MESSAGE)
    assert m(caplog) == FIRST_MESSAGE
    out, err = capsys.readouterr()
    assert out == FIRST_MESSAGE + "\n"
    assert not err


def test_formatted_output(caplog, capsys):
    log.set_default_format()
    log.debug("debug")
    assert m(caplog) == "debug"
    out, err = capsys.readouterr()
    assert out.endswith("debug\n")
    assert "DEBUG [tests.test_logx.test_formatted_output:" in out
    assert not err


def test_set_format(caplog, capsys):
    formatstring = '{ "timestamp": "%(asctime)s", "severity": "%(levelname)s", "name": "%(name)s", "funcName": "%(funcName)s", "lineNo": "%(lineno)d", "message": "%(message)s"}'
    datefmt = "%Y-%m-%dT%I:%M:%SZ"
    log.set_format(formatstring, datefmt=datefmt)
    log.debug("log stuff")
    output = json.loads(capsys.readouterr().out)
    assert datetime.strptime(output["timestamp"], datefmt) is not None
    assert output.keys() == json.loads(formatstring).keys()


def test_level_change_output(caplog, capsys):
    log.set_default_format()
    log.set_level("warn")
    log.warn("warn")
    log.debug("debug")
    out, err = capsys.readouterr()
    assert "warn" in err
    assert "debug" not in err and "debug" not in out


def test_null_handler(caplog, capsys):
    log.set_null_handler()
    log.warn("warn")
    log.debug("debug")
    out, err = capsys.readouterr()
    assert "warn" not in err and "warn" not in out
    assert "debug" not in err and "debug" not in out
    log.clear_null_handler()
    print_diagram()
    log.warn("warn")
    log.debug("debug")
    out, err = capsys.readouterr()
    assert "warn" in err and "warn" not in out
    assert "debug" not in err and "debug" in out
