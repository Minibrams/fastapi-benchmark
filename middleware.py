from fastapi import FastAPI
import threading

from starlette.requests import Request
from loguru import logger


def add_thread_logging_middleware(app: FastAPI):
    @app.middleware('http')
    async def log_thread_id(request: Request, call_next):

        thread_id = threading.get_ident()
        
        logger.info(f'Thread {thread_id} started handling a request ({threading.active_count()} threads currently active)')
        response = await call_next(request)
        logger.info(f'Thread {thread_id} finished handling a request (({threading.active_count()} threads currently active)')

        return response
