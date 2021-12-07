from starlette.responses import HTMLResponse
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import controllers.synchronous
import controllers.asynchronous


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


if __name__ == '__main__':

    uvicorn.run(
        'api:app',
        reload=True,
        host='0.0.0.0',
        port=4242
    )
