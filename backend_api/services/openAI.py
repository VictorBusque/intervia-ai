from json import load as jsonl
import logging
import openai
from os import getenv

from helpers.configuration import ConfigurationHelper
from models.redis import RedisUserData


class OpenAI(object):
    def __init__(self):
        openai.api_key = getenv("OPENAI_KEY")
        openai.organization = getenv("OPENAI_ORG")
        self.model = getenv("OPENAI_MODEL")
        self.config, _ = OpenAI.get_configuration()

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    @staticmethod
    def get_configuration():
        with open(f"configuration/{getenv('ENV')}/openai.json", "r", encoding="utf8") as f:
            config = jsonl(f)
        envs = {
            "OPENAI_KEY": config["credentials"]["key"],
            "OPENAI_ORG": config["credentials"]["org"],
            "OPENAI_MODEL": config["model"]["name"]
        }
        return config, envs

    def send_message(self,
                     user: str,
                     user_state: RedisUserData):
        logging.info(f"Sending message to {user}: \"{user_state.conversation[-1].content}\"")



        completion = openai.ChatCompletion.create(
            model=self.model,
            messages=[m.model_dump(mode="json") for m in user_state.conversation],
            temperature=self.config["prompt"]["temperature"],
            max_tokens=self.config["prompt"]["max_tokens"],
            top_p=self.config["prompt"]["top_p"]
        )
        response = completion.choices[0].message.content
        return response
