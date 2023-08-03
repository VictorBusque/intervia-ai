from typing import List, Optional

from pydantic import BaseModel

from models.linkedin import JobPost
from models.user import User
from models.gpt import GPTMessage


class Context(BaseModel):
    job_post: Optional[JobPost] = None


class RedisUserData(BaseModel):
    user: User
    conversation: List[GPTMessage]
    context: Context = Context()
