import os

import httpx
from fastapi import FastAPI, HTTPException

from main import KeyValue

app = FastAPI(
    title="proxy API",
    description="Proxy API for managing a high performance key-value store.",
    version="1.0.0",
)

### ConfigMap Variables
LEADER_URL = os.getenv("LEADER_URL", "http://kvstore-0.kvstore-service:8000")
KV_STORE_SERVICE_URL = os.getenv(
    "KV_STORE_SERVICE_URL",
    "http://kvstore-service:8000",
)


### API Endpoints
@app.put("/put")
async def proxy_put_key_value(data: KeyValue):
    """
    Proxy PUT requests to the leader.

    Args:
        data (KeyValue): The key-value pair to be added or updated.

    Returns:
        dict: Response from the leader node.
    """
    payload = {"key": data.key, "value": data.value}

    async with httpx.AsyncClient() as client:
        response = await client.put(f"{LEADER_URL}/put", json=payload)
    return response.json()


@app.delete("/delete/{key}")
async def proxy_delete_key(key: str):
    """
    Proxy DELETE requests to the leader.

    Args:
        key (str): The key to be deleted.

    Raises:
        HTTPException: If the key is not found or the request fails.

    Returns:
        dict: Response from the leader node.
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
    Proxy GET requests to the leader or replicas using round-robin.

    Args:
        key (str): The key to retrieve.

    Raises:
        HTTPException: If the key is not found.

    Returns:
        dict: The key-value pair retrieved from the store.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{KV_STORE_SERVICE_URL}/get/{key}")

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Key not found.")
    return response.json()
