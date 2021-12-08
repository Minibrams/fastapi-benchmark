import json
import aiofiles
import asyncio
from fastapi import APIRouter
from httpx import AsyncClient

router = APIRouter(prefix='/async')

client = AsyncClient(timeout=60)

@router.get('/json')
async def json_async():
    r = await client.get('https://jsonplaceholder.typicode.com/todos')
    await asyncio.sleep(1)
    return r.json()


@router.get('/http')
async def http_async():
    async with AsyncClient() as http:
        return (await http.get('https://jsonplaceholder.typicode.com/todos/1')).json()