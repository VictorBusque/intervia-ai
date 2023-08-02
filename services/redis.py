import logging
from typing import Dict, Any

import redis
from os import getenv
from json import load as jsonl
from json import dumps as jsonds
from json import loads as jsonls

from helpers.configuration import ConfigurationHelper
from models.gpt_completion import Completion
from models.user import User


class Redis(object):
    def __init__(self):
        self.engine = redis.Redis(host=getenv("REDIS_URL"), decode_responses=True)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    @staticmethod
    def get_configuration():
        with open("configuration/redis.json", "r", encoding="utf8") as f:
            config = jsonl(f)
        envs = {
            "REDIS_URL": config["url"]
        }
        ConfigurationHelper.load_config(envs)
        return config, envs

    def set(self, key: str, value: Any) -> None:
        self.logger.debug(f"Setting {key} to {value}")
        self.engine.set(key, value=value)

    def get(self, key: str) -> User:
        self.logger.debug(f"Getting {key}")
        user_data = self.engine.get(key)
        if user_data:
            return User(**jsonls(user_data))
        else:
            base_conversation = Completion.get_base_completion().messages
            user = User(id=key, conversation=base_conversation)
            self.set(key, jsonds(user.model_dump(mode="json")))
            return user

    def delete(self, key: str) -> None:
        self.logger.debug(f"Deleting {key}")
        self.engine.delete(key)
