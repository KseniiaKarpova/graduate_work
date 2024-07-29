from api.v1 import bot
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse


app = FastAPI(
    title="ASR",
    description="",
    docs_url='/asr/openapi',
    openapi_url='/asr/openapi.json',
    default_response_class=ORJSONResponse
)


app.include_router(bot.router, prefix='/asr/api/v1/audio', tags=['audio'])
