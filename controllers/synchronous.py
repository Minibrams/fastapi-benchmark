import json
import requests
import time
from fastapi import APIRouter
from httpx import Client

router = APIRouter(prefix='/sync')

@router.get('/json')
def json_sync():
    with Client() as http:
        time.sleep(1)
        return http.get('https://jsonplaceholder.typicode.com/todos').json()


@router.get('/http')
def http_sync():
    with Client() as http:
        return http.get('https://jsonplaceholder.typicode.com/todos/1').json()