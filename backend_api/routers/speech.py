from os import getenv
from typing import Dict
from typing_extensions import Annotated
from fastapi import APIRouter, File, Query, status, Depends, Body, Path
from models.response import STTResponse

from services.speech import Speech


router = APIRouter()

@router.post("/stt", response_model=STTResponse, status_code=status.HTTP_200_OK)
async def post_file(file: Annotated[bytes, File()]) -> STTResponse:
    transcription = Speech.stt(file)
    return STTResponse(**{"text": transcription})



@router.get("/tts", response_model=bytes, status_code=status.HTTP_200_OK)
async def post_tts(text: str = Query(...)) -> File:
    audio_file = Speech.tts(text)
    return audio_file
