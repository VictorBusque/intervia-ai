import logging
from typing import Any, Union

import redis
from os import getenv
from json import load as jsonl
from json import loads as jsonls

from helpers.configuration import ConfigurationHelper
from models.redis import RedisUserData


class Redis(object):
    def __init__(self):
        self.engine = redis.Redis(host=getenv("REDIS_URL"), decode_responses=True)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    @staticmethod
    def get_configuration():
        with open(f"configuration/{getenv('ENV')}/redis.json", "r", encoding="utf8") as f:
            config = jsonl(f)
        envs = {
            "REDIS_URL": config["url"]
        }
        return config, envs

    def set(self, key: str, value: Any) -> None:
        self.logger.debug(f"Setting user data for {key} to {value}")
        self.engine.set(key, value=value)

    def get(self, key: str) -> Union[RedisUserData, None]:
        self.logger.debug(f"Getting user data for {key}")
        user_data = self.engine.get(key)
        if user_data:
            self.logger.debug(f"Found user data for {key}")
            return RedisUserData(**jsonls(user_data))
        else: 
            self.logger.warning(f"No user data found for: {key}")
            return None


    def delete(self, key: str) -> None:
        self.logger.debug(f"Deleting user data for: {key}")
        self.engine.delete(key)
