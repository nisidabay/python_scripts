#!/usr/bin/python3
import asyncio
import timeit
from async_utils.delay import delay
from async_utils.async_timed import async_timed


@async_timed()
async def task1():
    print("Send first Email")
    asyncio.create_task(task2())
    await delay(5)
    print("First Email reply")


@async_timed()
async def task2():
    print("Send second Email")
    asyncio.create_task(task3())
    await delay(2)
    print("Second Email reply")


@async_timed()
async def task3():
    print("Send third Email")
    await delay(1)
    print("Third Email reply")


t = timeit.timeit("asyncio.run(task1())", globals=globals(), number=1)
print(f"time elapsed: {t}")
