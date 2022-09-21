
gunicorn --bind 127.0.0.1:8000 -w 4 -k uvicorn.workers.UvicornWorker echo_service.core:app
