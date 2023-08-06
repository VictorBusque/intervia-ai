from models.linkedin import JobPost
from models.gpt import GPTMessage
from pydantic import BaseModel


class ConversationResponse(BaseModel):
    response: GPTMessage
    job_post: JobPost
    
    
class STTResponse(BaseModel):
    text: str
