from typing import List

from pydantic import BaseModel

from models.gpt_completion import GPTMessage


class User(BaseModel):
    id: str
    conversation: List[GPTMessage]