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
        if jobdata:
            return cls(**jobdata)
        else:
            logging.error("Could not connect and get description from LinkedIn URL.")
            return None
