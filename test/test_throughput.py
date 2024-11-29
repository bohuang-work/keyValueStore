import time
import httpx
import asyncio

BASE_URL = "http://127.0.0.1:54452"

# Custom timeout and connection settings
TIMEOUT = httpx.Timeout(
    100.0, connect=10.0
)  # Total timeout: 100s, connection timeout: 50s
MAX_CONNECTIONS = 20  # Limit connections to avoid overloading the service


async def put_request(client, key, value):
    """Send a PUT request to add a key-value pair."""
    try:
        response = await client.put(
            f"{BASE_URL}/put", json={"key": key, "value": value}
        )
        return response.status_code, response.text
    except httpx.RequestError as e:
        return "Error", str(e)


async def get_request(client, key):
    """Send a GET request to retrieve a value by key."""
    try:
        response = await client.get(f"{BASE_URL}/get/{key}")
        return response.status_code, response.json()
    except httpx.RequestError as e:
        return "Error", str(e)
    except httpx.HTTPStatusError:
        return response.status_code, response.text


async def test_throughput():
    # Limit connections to avoid overwhelming the service
    limits = httpx.Limits(
        max_connections=MAX_CONNECTIONS, max_keepalive_connections=MAX_CONNECTIONS
    )
    async with httpx.AsyncClient(timeout=TIMEOUT, limits=limits) as client:
        # Step 1: Perform a single PUT request to set the key
        key = "test-key"
        value = "test-value"
        put_status, put_response = await put_request(client, key, value)
        print(f"PUT request completed with status {put_status}: {put_response}")

        if put_status != 200:
            print("Failed to set the key. Exiting test.")
            return

        # Step 2: Simulate 100 GET requests for the same key
        tasks = [get_request(client, key) for _ in range(50)]

        # Record the start time
        start_time = time.time()

        # Run all GET requests concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Record the end time
        end_time = time.time()

        # Calculate the time taken to process the requests
        time_taken = end_time - start_time
        total_requests = len(tasks)

        # Calculate throughput (requests per second)
        throughput = total_requests / time_taken

        print(f"Completed {total_requests} GET requests in {time_taken:.2f} seconds.")
        print(f"Throughput: {throughput:.2f} requests per second.")

        # Display the first few responses for verification
        for i, result in enumerate(results[:5]):  # Show first 5 responses
            print(f"GET request {i + 1}: {result}")


# Run the test
asyncio.run(test_throughput())
