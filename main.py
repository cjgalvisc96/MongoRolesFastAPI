from app.core.config import settings
from app.create_app import create_app

app = create_app(settings)


if __name__ == "__main__":
    import asyncio

    import uvicorn

    loop = asyncio.get_event_loop()
    config = uvicorn.Config(app=app, port=settings.APP_PORT, loop=loop)
    server = uvicorn.Server(config)
    loop.run_until_complete(server.serve())
