from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings
from app.core.db import mongo_db
from app.db.init_db import init_db


def add_db(app, config_db):
    mongo_db.uri = config_db.MONGO_DATABASE_URI
    mongo_db.db_name = config_db.DB_NAME

    @app.on_event("startup")
    async def startup() -> None:
        app.state.db_instance = mongo_db.init_db()
        await init_db()  # Add initial data


def ping_router(app):
    @app.get("/ping")
    def get_ping():
        return {"result": "pong"}


def add_routers(app):
    ping_router(app)
    app.include_router(api_router, prefix=settings.API_V1_PREFIX)


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
