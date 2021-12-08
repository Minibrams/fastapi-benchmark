from starlette.responses import HTMLResponse
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import controllers.synchronous
import controllers.asynchronous

from flask import Flask
from httpx import Client

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(controllers.synchronous.router)
app.include_router(controllers.asynchronous.router)


# app = Flask(__name__)

# @app.route("/sync/json/")
# def hello_world():
#     with Client() as http:
#         r = http.get('https://jsonplaceholder.typicode.com/todos')
#         return "Blah"

