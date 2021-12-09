import json
import threading
from fastapi import APIRouter
from httpx import Client
from loguru import logger


router = APIRouter(prefix='/sync')

@router.get('/json')
def json_sync():
    with open('data.json') as fp:
        return json.loads(fp.read())


@router.get('/http')
def http_sync():
    with Client() as http:
        return http.get('http://165.227.149.214:8090?waitms=1000').content
