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
        app.state.client = AsyncIOMotorClient(
            config_db.MONGO_DATABASE_URI, io_loop=loop
        )
        app.state.db = app.state.client[config_db.DB_NAME]
        app.state.db_instance.set_db(app.state.db)


def ping_router(app):
    @app.get("/ping")
    def get_ping():
        return {"result": "pong"}


def add_routers(app):
    ping_router(app)
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
        openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    )
    add_routers(app)
    add_db(app, settings)
    add_middleware(app)
    return app
