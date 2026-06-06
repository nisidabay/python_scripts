#!/usr/bin/python3

# Ways to run coroutines
# With Tasks the coroutines are running concurrently

import asyncio
from async_utils import delay, async_timed


async def waiter() -> None:
    task1 = asyncio.create_task(cook("Pasta", 5))
    task2 = asyncio.create_task(cook("Caesar Saladad", 3))
    task3 = asyncio.create_task(cook("Lamb Chops", 6))

    await task1
    await task2
    await task3


@async_timed()
async def cook(order: str, time_to_prepare: int) -> None:
    print(f"Getting {order} order")
    await delay(time_to_prepare)
    print(f"{order} ready")


if __name__ == "__main__":
    asyncio.run(waiter())
