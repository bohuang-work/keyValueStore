from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from key_value_store import KeyValueStore

app = FastAPI(
    title="kvStore API",
    description="API for managing a simple key-value store.",
    version="1.0.0",
)

# Initialize the shared KeyValueStore
kv_store = KeyValueStore()


### Model
class KeyValue(BaseModel):
    key: str
    value: str


### API Endpoints
@app.put("/put")
async def put_key_value(data: KeyValue):
    """
    Add or update a key-value pair in the store.
    """
    kv_store.put(data.key, data.value)
    return {"message": f"Key '{data.key}' added/updated successfully."}


@app.delete("/delete/{key}")
async def delete_key(key: str):
    """
    Delete a key-value pair from the store.
    """
    if kv_store.delete(key):
        return {"message": f"Key '{key}' deleted successfully."}
    else:
        raise HTTPException(status_code=404, detail="Key not found.")


@app.get("/get/{key}")
async def get_key_value(key: str):
    """
    Retrieve the value associated with a key.
    """
    value = kv_store.get(key)
    if value is None:
        raise HTTPException(status_code=404, detail="Key not found.")
    return {"key": key, "value": value}
