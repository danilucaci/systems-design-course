"""A local scheduling experiment, not a network or throughput benchmark."""

import asyncio
import json


async def probe(requests: int, limit: int) -> dict[str, int]:
    if type(requests) is not int or type(limit) is not int:
        raise ValueError("requests and limit must be integers")
    if not 0 <= requests <= 10_000 or not 1 <= limit <= 10_000:
        raise ValueError("requests must be 0..10000 and limit must be 1..10000")
    gate = asyncio.Semaphore(limit)
    active = maximum = completed = 0

    async def operation():
        nonlocal active, maximum, completed
        async with gate:
            active += 1
            maximum = max(maximum, active)
            try:
                await asyncio.sleep(0)
                completed += 1
            finally:
                active -= 1

    await asyncio.gather(*(operation() for _ in range(requests)))
    return {"completed": completed, "maximum_active": maximum}


async def main():
    for limit in (1, 2, 10):
        result = await probe(requests=10, limit=limit)
        print(json.dumps({"limit": limit, **result}))


if __name__ == "__main__":
    asyncio.run(main())
