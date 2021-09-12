import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient


from app.db.session import db_instance


def add_db(app, config_db):
    app.state.db_instance = db_instance

    @app.on_event("startup")
    async def startup() -> None:
        loop = asyncio.get_event_loop()
        app.state.client = AsyncIOMotorClient(config_db.mongo_host, config_db.mongo_port, io_loop=loop)
        app.state.db = app.state.client[config_db.mongo_db]
        app.state.db_instance.set_db(app.state.db)


def add_routers(app):
    @app.get("/ping")
    def get_ping():
        return {"result": "pong"}
    # app.include_router(app.router, prefix=settings.API_V1_PREFIX)


def add_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def create_app(settings):
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
    )
    add_routers(app)
    add_db(app, settings)
    add_middleware(app)
    return app
