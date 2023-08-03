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


from models.redis import Context


class Completion(BaseModel):
    model: str
    messages: List[GPTMessage]

    @staticmethod
    def get_base_completion(context: Context = None):
        from services.openAI import OpenAI
        openai_config, _ = OpenAI.get_configuration()

        if context:
            jobpost_prompt = f"\nTitle: {context.job_post.title}\nDescription: {context.job_post.description}\n"
        else:
            jobpost_prompt = ""

        return Completion(
            model=getenv("OPENAI_MODEL"),
            messages=[
                GPTMessage(role=Role.system, content=openai_config["prompt"]["system"] + jobpost_prompt),
            ]
        )
