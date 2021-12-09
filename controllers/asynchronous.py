import json
import aiofiles
import threading
from fastapi import APIRouter
from httpx import Client, AsyncClient
from loguru import logger


router = APIRouter(prefix='/async')


@router.get('/json')
async def json_async():
    async with aiofiles.open('data.json') as fp:
        return json.loads(await fp.read())


@router.get('/http')
async def http_async():
    async with AsyncClient() as http:
        return (await http.get('http://165.227.149.214:8090?waitms=1000')).content


@router.get('/http/sync')
async def http_async():
    with Client() as http:
        return http.get('http://165.227.149.214:8090?waitms=1000').content
    
