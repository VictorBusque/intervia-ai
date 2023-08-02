from pydantic import BaseModel


class JobPost(BaseModel):
    title: str
    description: str
    company: str
    url: str
