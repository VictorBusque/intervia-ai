from typing_extensions import Annotated
from fastapi import APIRouter, File, Query, status, Response
from models.response import STTResponse

from services.speech import Speech

router = APIRouter()


@router.post("/stt", response_model=STTResponse, status_code=status.HTTP_200_OK)
async def post_file(file: Annotated[bytes, File()]) -> STTResponse:
    transcription = Speech.stt(file)
    return STTResponse(**{"text": transcription})


@router.get("/tts", status_code=status.HTTP_200_OK)
async def post_tts(text: str = Query(...)) -> Response:
    audio_file = Speech.tts(text)
    return Response(audio_file, media_type="audio/wav")
