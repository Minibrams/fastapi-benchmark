import json
import aiofiles
from fastapi import APIRouter
from httpx import AsyncClient

router = APIRouter(prefix='/async')

@router.get('/json')
async def json_async():
    async with aiofiles.open('data.json') as fp:
        return json.loads(await fp.read())

@router.get('/http')
async def http_async():
    async with AsyncClient() as http:
        return (await http.get('https://jsonplaceholder.typicode.com/todos/1')).json()