from typing import Optional
from fastapi import FastAPI, Request, BackgroundTasks
import httpx

app = FastAPI()

async def reply(payload):
    print("here")
    url = "https://client0001.pythonanywhere.com/wati_whatsapp"

    try:
        print("Are you there")
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            print("Request sent")
    except Exception as e:
        print("request failed:", e)

@app.post("/whatsapp")
async def root(request: Request, background_tasks: BackgroundTasks):
    # Parse incoming request JSON
    body = await request.json()
    
    question = str(body.get("text", ""))
    contactnum = str(body.get("waId", "errresponse"))
    sendername = str(body.get("senderName", ""))
    
    background_tasks.add_task(reply, body)

    return "Success!"
    
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
