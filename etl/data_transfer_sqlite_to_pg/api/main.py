from concurrent.futures import ThreadPoolExecutor

from api.sqlite_to_postgres.load_data import run
from dotenv import load_dotenv
from fastapi import FastAPI

executor = ThreadPoolExecutor(max_workers=3)
app = FastAPI(
    description="Information about films, genres and actors",
    docs_url='/data_transfer/openapi',
    openapi_url='/data_transfer/openapi.json',
)
load_dotenv()


@app.get("/data_transfer/")
def main_page():
    return 'Data Transfer (from sqlite to postgres)'


@app.get("/data_transfer/migrate")
def migrate_from_sqlite_to_postgres():
    executor.submit(run)
    return {"result": "Start migrate data"}
