"""
from typing import Optional
from fastapi import FastAPI, Request, BackgroundTasks
import httpx

app = FastAPI()

async def reply(request: Request):
    url = "https://client0001.pythonanywhere.com/wati_whatsapp"
    try:
        body = await request.json()
        async with httpx.AsyncClient() as client:
            await client.post(url, json=body)
    except Exception as e:
        print("There was error sending the request")
    return {"message": "Success!"}

@app.post("/whatsapp")
async def root(request: Request, background_tasks: BackgroundTasks):
    background_tasks.add_task(reply, request)
    return {"message": "Success!"}
"""
from fastapi import FastAPI, Request, BackgroundTasks, HTTPException
import httpx
import asyncio

app = FastAPI()

async def reply(request: Request):
    url = "https://client0001.pythonanywhere.com/wati_whatsapp"
    try:
        body = await request.json()
        async with httpx.AsyncClient() as client:
            await asyncio.wait_for(client.post(url, json=body), timeout=3)
    except asyncio.TimeoutError:
        return {"message": "Success!"}
    except Exception as e:
        print("There was error sending the request")
    return {"message": "Success!"}

@app.post("/whatsapp")
async def root(request: Request, background_tasks: BackgroundTasks):
    try:
        await asyncio.wait_for(asyncio.create_task(reply(request)), timeout=2)
    except asyncio.TimeoutError:
        return {"message": "Success!"}
    return {"message": "Success!"}
