import logging
from typing import Dict
import os
from json import load as jsonl


class ConfigurationHelper(object):
    @staticmethod
    def load_config(env_vars: Dict) -> None:
        # This function loads the env vars from the parameter as environment variables.
        logging.info(f"Loading env: {list(env_vars.keys())}")
        for key, value in env_vars.items():
            os.environ[key] = value

    @staticmethod
    def load_base_config():
        logging.info("Loading base configuration...")
        with open(f"configuration/{os.getenv('ENV')}/base.json", "r", encoding="utf8") as f:
            base_config = jsonl(f)
        ConfigurationHelper.load_config(base_config)
