from fastapi import Header, HTTPException
import os

API_KEY = os.environ.get("API_KEY")

async def get_api_key(api_key: str = Header(...)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return api_key