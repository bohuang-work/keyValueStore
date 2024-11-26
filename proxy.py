import os

import httpx
from fastapi import FastAPI, HTTPException

from main import KeyValue

app = FastAPI(
    title="Proxy API",
    description="This API proxies requests to the leader or replica services.",
    version="1.0.0",
)

# URLs are passed via environment variables
LEADER_URL = os.getenv("LEADER_URL", "http://kvsotre/:8000")
REPLICA_SERVICE_URL = os.getenv("REPLICA_SERVICE_URL", "http://kvsotre/:8000")


@app.put("/put")
async def proxy_put_key_value(data: KeyValue):
    """
    Proxy PUT requests to the leader.
    """
    payload = {"key": data.key, "value": data.value}

    async with httpx.AsyncClient() as client:
        response = await client.put(f"{LEADER_URL}/put", json=payload)
    return response.json()


@app.delete("/delete/{key}")
async def proxy_delete_key(key: str):
    """
    Proxy DELETE requests to the leader and handle 404 responses.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.delete(f"{LEADER_URL}/delete/{key}")
            # If the leader returns 404 (key not found), raise an exception
            if response.status_code == 404:
                raise HTTPException(status_code=404, detail="Key not found.")
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")


@app.get("/get/{key}")
async def proxy_get_key_value(key: str):
    """
    Proxy GET requests to the replica or leader service and handle 404 responses.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{REPLICA_SERVICE_URL}/get/{key}")
            # If the leader also returns 404 (key not found), raise an exception
            if response.status_code == 404:
                raise HTTPException(status_code=404, detail="Key not found.")

            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")
