from os import getenv

from fastapi import FastAPI
import uvicorn
import logging
from dotenv import load_dotenv

from helpers.configuration import ConfigurationHelper
from services.linkedin import LinkedIn
from services.redis import Redis
from services.openAI import OpenAI
load_dotenv()


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("uvicorn")

app = FastAPI(title=f"Simujob")

from routers import conversation

@app.on_event("startup")
async def startup():
    logger.info("Starting Simujob")
    ConfigurationHelper.load_base_config()
    for service in [Redis, OpenAI, LinkedIn]:
        config, envs = service.get_configuration()
        ConfigurationHelper.load_config(envs)

app.include_router(conversation.router,
                   prefix="/conversation",
                   tags=["Conversation"])

if __name__ == "__main__":
    from asyncio import run
    run(startup())
    PORT = getenv("PORT")
    uvicorn.run(app, host="0.0.0.0", port=int(PORT))
