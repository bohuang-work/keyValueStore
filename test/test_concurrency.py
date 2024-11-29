import asyncio
import httpx

BASE_URL = "http://127.0.0.1:54452"

# Helper function to process server responses
async def handle_response(response):
    try:
        response_json = response.json()
        return response.status_code, response_json
    except ValueError:
        return response.status_code, {"error": "Invalid JSON", "content": response.text}


# Function to perform a PUT request
async def put_request(client, key, value):
    try:
        response = await client.put(
            f"{BASE_URL}/put", json={"key": key, "value": value}
        )
        return await handle_response(response)
    except httpx.RequestError as e:
        return None, {"error": "Request failed", "details": str(e)}


# Function to perform a GET request
async def get_request(client, key):
    try:
        response = await client.get(f"{BASE_URL}/get/{key}")
        return await handle_response(response)
    except httpx.RequestError as e:
        return None, {"error": "Request failed", "details": str(e)}


# Function to perform a DELETE request
async def delete_request(client, key):
    try:
        response = await client.delete(f"{BASE_URL}/delete/{key}")
        return await handle_response(response)
    except httpx.RequestError as e:
        return None, {"error": "Request failed", "details": str(e)}


# Test function for sequential operations
async def test_concurrent_clients():
    # Set a higher timeout
    timeout = httpx.Timeout(
        10.0, connect=5.0
    )  # 10 seconds total, 5 seconds for connection
    async with httpx.AsyncClient(timeout=timeout) as client:
        # Step 1: Perform 10 PUT requests
        put_tasks = [put_request(client, f"key-{i}", f"value-{i}") for i in range(10)]
        put_results = await asyncio.gather(*put_tasks)
        print("\nPUT Results:")
        for i, result in enumerate(put_results):
            print(f"PUT Task {i + 1}: {result}")

        # Wait for 2 seconds
        await asyncio.sleep(0.5)

        # Step 2: Perform 10 GET requests
        get_tasks = [get_request(client, f"key-{i}") for i in range(10)]
        get_results = await asyncio.gather(*get_tasks)
        print("\nGET Results:")
        for i, result in enumerate(get_results):
            print(f"GET Task {i + 1}: {result}")

        # Step 3: Perform 10 DELETE requests
        delete_tasks = [delete_request(client, f"key-{i}") for i in range(10)]
        delete_results = await asyncio.gather(*delete_tasks)
        print("\nDELETE Results:")
        for i, result in enumerate(delete_results):
            print(f"DELETE Task {i + 1}: {result}")

        # Wait for 2 seconds
        await asyncio.sleep(0.5)

        # Step 4: Perform 10 GET requests again
        final_get_tasks = [get_request(client, f"key-{i}") for i in range(10)]
        final_get_results = await asyncio.gather(*final_get_tasks)
        print("\nFinal GET Results (after DELETE):")
        for i, result in enumerate(final_get_results):
            print(f"Final GET Task {i + 1}: {result}")


# Run the test
if __name__ == "__main__":
    asyncio.run(test_concurrent_clients())
