from json import loads as jsonls
import requests
from os import getenv


class Speech(object):
    @staticmethod
    def get_configuration():
        with open(f"configuration/{getenv('ENV')}/tts.json", "r", encoding="utf8") as f:
            tts_config = jsonls(f.read())
        with open(f"configuration/{getenv('ENV')}/stt.json", "r", encoding="utf8") as f:
            stt_config = jsonls(f.read())
        config = {
            "stt": stt_config,
            "tts": tts_config
        }
        envs = {
            "TTS_API_URL": tts_config["url"],
            "STT_API_URL": stt_config["url"]
        }
        return config, envs
    
    @staticmethod
    def stt(file: bytes) -> str:
        params = {
            "task": "transcribe",
            "language": "en",
            "encode": True,
            "output": "json"
        }
        response = requests.post(f"{getenv('STT_API_URL')}/asr", params=params, files={"audio_file": file})
        response.raise_for_status()
        response_json = response.json()
        transcription = response_json.get("text")
        return transcription
    
    @staticmethod
    def tts(text: str) -> bytes:
        config, _ = Speech.get_configuration()
        text = text.replace("Score", "")
        url = f"{getenv('TTS_API_URL')}/api/tts?text={text}&lengthScale={config['tts'].get('length_scale')}"
        response = requests.get(url)
        response.raise_for_status()
        file = bytes(response.content)
        return file