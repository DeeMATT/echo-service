import uvicorn

from fastapi import Depends
from echo_service.core import config, Settings


def main(settings: Settings = Depends(config)):
    uvicorn.run(
        app="echo_service.core:app",
        host=config.APP_HOST,
        port=config.APP_PORT,
        reload=True if config.ENV != "prod" else False,
        workers=1,
    )


if __name__ == "__main__":
    main()
