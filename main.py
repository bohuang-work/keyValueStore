import asyncio
import os

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from key_value_store import KeyValueStore

app = FastAPI(
    title="kvStore API",
    description="API for managing a high performance key-value store.",
    version="1.0.0",
)

# Initialize the shared KeyValueStore
kv_store = KeyValueStore()


### Model
class KeyValue(BaseModel):
    key: str
    value: str


### ConfigMap
REPLICA_URLS = os.getenv(
    "REPLICA_URLS",
    "http://kvstore-1.kvstore-service:8000,http://kvstore-2.kvstore-service:8000,http://kvstore-3.kvstore-service:8000,http://kvstore-4.kvstore-service:8000",
).split(",")

POD_NAME = os.getenv("POD_NAME", "")
REPLICA_COUNT = os.getenv("REPLICA_COUNT", 1)


### Helper function to notify replicas
async def notify_replicas(endpoint: str, data: dict):
    """
    Notify replicas of a change in the store.

    Args:
        endpoint (str): The endpoint to call on replicas (e.g., "put" or "delete").
        data (dict): The data payload to send to replicas.

    Returns:
        None
    """
    async with httpx.AsyncClient() as client:
        # Notify each replica about the change (PUT or DELETE)
        tasks = []
        for replica_url in REPLICA_URLS:
            if endpoint == "put":
                task = client.put(f"{replica_url}/put", json=data)
            elif endpoint == "delete":
                task = client.delete(f"{replica_url}/delete/{data['key']}")
            tasks.append(task)
        # Wait for all tasks to complete
        await asyncio.gather(*tasks)


### API Endpoints
@app.put("/put")
async def put_key_value(data: KeyValue):
    """
    Add or update a key-value pair in the store.

    Args:
        data (KeyValue): The key-value pair to be added or updated.

    Returns:
        dict: A message confirming the addition or update of the key-value pair.
    """
    kv_store.put(data.key, data.value)

    # Ensure only the leader (kvstore-0) notifies replicas
    if POD_NAME == "kvstore-0" and REPLICA_COUNT > 1:
        # Notify replicas about the update
        await notify_replicas(
            endpoint="put", data={"key": data.key, "value": data.value}
        )

    return {"message": f"Key '{data.key}' added/updated successfully."}


@app.delete("/delete/{key}")
async def delete_key(key: str):
    """
    Delete a key-value pair from the store.

    Args:
        key (str): The key to be deleted.

    Raises:
        HTTPException: If the key is not found.

    Returns:
        dict: A message confirming the deletion of the key-value pair.
    """
    if kv_store.delete(key):
        if POD_NAME == "kvstore-0" and REPLICA_COUNT > 1:
            await notify_replicas(endpoint="delete", data={"key": key})
        return {"message": f"Key '{key}' deleted successfully."}
    else:
        raise HTTPException(status_code=404, detail="Key not found.")


@app.get("/get/{key}")
async def get_key_value(key: str):
    """
    Retrieve the value associated with a key.

    Args:
        key (str): The key to retrieve.

    Raises:
        HTTPException: If the key is not found.

    Returns:
        dict: The key-value pair retrieved from the store.
    """
    value = kv_store.get(key)
    if value is None:
        raise HTTPException(status_code=404, detail="Key not found.")
    return {"key": key, "value": value}
