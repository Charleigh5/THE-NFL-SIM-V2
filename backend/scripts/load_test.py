import asyncio
import time
import statistics
import sys

try:
    import aiohttp
except ImportError:
    print("aiohttp is required. Please install it with: pip install aiohttp")
    sys.exit(1)

async def make_request(session, url):
    start = time.time()
    try:
        async with session.get(url) as response:
            await response.text()
            return time.time() - start, response.status
    except Exception as e:
        return time.time() - start, 0

async def load_test():
    url = "http://localhost:8000/" # Root endpoint
    concurrency = 100
    total_requests = 1000

    print(f"Starting load test on {url}")
    print(f"Concurrency: {concurrency}")
    print(f"Total Requests: {total_requests}")

    async with aiohttp.ClientSession() as session:
        semaphore = asyncio.Semaphore(concurrency)

        async def bounded_request():
            async with semaphore:
                return await make_request(session, url)

        bounded_tasks = [bounded_request() for _ in range(total_requests)]

        start_total = time.time()
        results = await asyncio.gather(*bounded_tasks)
        total_time = time.time() - start_total

        latencies = [r[0] * 1000 for r in results]
        statuses = [r[1] for r in results]

        success_count = statuses.count(200)

        print("\nLoad Test Results:")
        print(f"Total Time: {total_time:.2f}s")
        print(f"Requests/sec: {total_requests / total_time:.2f}")
        print(f"Successful Requests: {success_count}/{total_requests}")
        print(f"Average Latency: {statistics.mean(latencies):.2f}ms")
        if len(latencies) >= 20:
            print(f"P95 Latency: {statistics.quantiles(latencies, n=20)[18]:.2f}ms")
        print(f"Max Latency: {max(latencies):.2f}ms")

if __name__ == "__main__":
    asyncio.run(load_test())
