#!/usr/bin/python3

# Ways to run coroutines with asyncio.gather()

import asyncio
import timeit


async def waiter() -> None:
    task1 = asyncio.create_task(cook("Pasta", 0.8))
    task2 = asyncio.create_task(cook("Caesar Saladad", 0.3))
    task3 = asyncio.create_task(cook("Lamb Chops", 0.16))

    await asyncio.gather(task1, task2, task3)


async def cook(order: str, time_to_prepare: float) -> None:
    print(f"Getting {order} order")
    await asyncio.sleep(time_to_prepare)
    print(order, "ready")


if __name__ == "__main__":
    t = timeit.timeit("asyncio.run(waiter())", globals=globals(), number=1)
    print(t)
