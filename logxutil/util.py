import io
import os
import yaml

from logx import log


log.set_null_handler("logxutil")

ENV_YAML = ".env.yaml"


def load_env_yaml(path=None):
    path = path or ENV_YAML

    try:
        with io.open(path) as r:
            log.info(f"loading env vars from yaml: {path}")
            env_vars = yaml.load(r, Loader=yaml.FullLoader)
            os.environ.update(env_vars)
    except FileNotFoundError:
        log.info(f"local env file not found at {path}, not loading")


def env(name):
    return os.environ[name]
