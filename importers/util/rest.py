import json
from urllib import request

headers = {
    'Content-Type': 'application/json'
}


def get(url: str) -> dict:
    req = request.Request(url, headers=headers)
    resp = request.urlopen(req)
    return json.loads(resp.read().decode())


def post(url: str, body: dict) -> dict:
    req = request.Request(url, data=json.dumps(body).encode('utf-8'), headers=headers)
    resp = request.urlopen(req)
    return json.loads(resp.read().decode())
