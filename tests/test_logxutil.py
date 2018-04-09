import logxutil
from logx import log
from pytest import raises


def m(caplog):
    return caplog.records[-1].message


def test_env(caplog, capsys):
    log.clear_null_handler(name="logxutil")
    logxutil.load_env_yaml("tests/test_env_yaml")
    assert "loading env vars" in m(caplog)
    assert logxutil.env("ABC") == "def"


def test_env_file_not_found(caplog, capsys):
    log.clear_null_handler(name="logxutil")
    logxutil.load_env_yaml("tests/test_env_yaml_bad")
    assert "local env file not found" in m(caplog)

    with raises(KeyError):
        logxutil.env("BAD")
