import logging

from pydantic import BaseModel
from services.linkedin import LinkedIn


class JobPost(BaseModel):
    title: str
    description: str
    company: str
    url: str

    @classmethod
    def from_url(cls, url: str) -> "JobPost":
        jobdata = LinkedIn.extract_job_data(url)
        return cls(**jobdata)
