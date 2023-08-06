from typing import Dict

from fastapi import APIRouter, status, Depends, Body, Path
from helpers.message_helper import get_linkedin_jobpost_url
from models.gpt import GPTMessage, Role, Completion
from models.linkedin import JobPost
from models.redis import Context, RedisUserData
from models.response import ConversationResponse
from models.user import User
from services.openAI import OpenAI
from services.redis import Redis
from json import dumps as jsonds

router = APIRouter()


@router.delete("/{user_id}/", response_model=None, status_code=status.HTTP_200_OK)
def post_message(user_id: str = Path(...),
                 redis_service: Redis = Depends(Redis)) -> None:
    redis_service.delete(user_id)


@router.post("/{user_id}/message", response_model=ConversationResponse, status_code=status.HTTP_200_OK)
def post_message(user_id: str = Path(...),
                 message: Dict = Body(...),
                 redis_service: Redis = Depends(Redis),
                 openai: OpenAI = Depends(OpenAI)) -> ConversationResponse:
    message_text = message.get("text")
    user_state = redis_service.get(user_id)

    job_post_url = get_linkedin_jobpost_url(message_text)
    if job_post_url:
        message_text = job_post_url
    if not job_post_url and not user_state:
        return ConversationResponse(**{
            "response": GPTMessage(role=Role.assistant, content="I need you to send me a LinkedIn job post link, such as https://www.linkedin.com/jobs/view/1234567890/"),
            "job_post": None
        })

    elif job_post_url and not user_state:
        user = User(id=user_id, email=None)
        job_post = JobPost.from_url(job_post_url)
        if job_post:
            context = Context(job_post=JobPost.from_url(job_post_url))
            conversation = Completion.get_base_completion(context).messages
            user_state = RedisUserData(user=user, conversation=conversation, context=context)
            redis_service.set(user_id, jsonds(user_state.model_dump(mode="json")))
        else:
            return ConversationResponse(**{
            "response": GPTMessage(role=Role.assistant, content="I could not load the LinkedIn job post. Try again later or with another job post."),
            "job_post": None
        })

    if user_state.context.job_post:
        if not job_post_url:
            user_state.conversation.append(GPTMessage(role=Role.user, content=message_text))

        response = openai.send_message(user_id, user_state)
        response_message = GPTMessage(role=Role.assistant, content=response)
        user_state.conversation.append(response_message)
        redis_service.set(user_id, jsonds(user_state.model_dump(mode="json")))
        return ConversationResponse(**{
            "response": response_message,
            "job_post": user_state.context.job_post
        })
