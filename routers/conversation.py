from typing import Dict

from fastapi import APIRouter, status, Depends, Body, Path

from models.gpt_completion import GPTMessage, Role
from services.openAI import OpenAI
from services.redis import Redis
from json import dumps as jsonds

router = APIRouter()


@router.delete("/{user_id}/", response_model=None, status_code=status.HTTP_200_OK)
def post_message(user_id: str = Path(...),
                 redis_service: Redis = Depends(Redis)) -> None:
    redis_service.delete(user_id)


@router.post("/{user_id}/message", response_model=GPTMessage, status_code=status.HTTP_200_OK)
def post_message(user_id: str = Path(...),
                 message: Dict = Body(...),
                 redis_service: Redis = Depends(Redis),
                 openai: OpenAI = Depends(OpenAI)) -> GPTMessage:
    message_text = message.get("text")

    user_state = redis_service.get(user_id)
    user_state.conversation.append(GPTMessage(role=Role.user, content=message_text))

    response = openai.send_message(user_id, user_state)
    response_message = GPTMessage(role=Role.assistant, content=response)
    user_state.conversation.append(response_message)
    redis_service.set(user_id, jsonds(user_state.model_dump(mode="json")))
    return response_message
