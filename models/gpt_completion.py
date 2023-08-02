from typing import List

from pydantic import BaseModel
from enum import Enum
from os import getenv


class Role(str, Enum):
    system = "system"
    user = "user"
    assistant = "assistant"


class GPTMessage(BaseModel):
    role: Role
    content: str


class Completion(BaseModel):
    model: str
    messages: List[GPTMessage]

    @staticmethod
    def get_base_completion():
        from services.openAI import OpenAI
        openai_config, _ = OpenAI.get_configuration()
        return Completion(
            model=getenv("OPENAI_MODEL"),
            messages=[
                GPTMessage(role=Role.system, content=openai_config["prompt"]["system"] + openai_config["prompt"]["job_post"]),
            ]
        )
