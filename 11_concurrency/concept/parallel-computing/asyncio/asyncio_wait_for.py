#!/usr/bin/python3
""" Setting a timeout and cancelling with wait for """
import asyncio
from async_utils import delay, async_timed


@async_timed()
async def main():
    threshold = 5
    long_task = asyncio.create_task(delay(10))
    try:
        await asyncio.wait_for(long_task, timeout=threshold)
    except asyncio.exceptions.TimeoutError:
        print(f"Got a timeout of {threshold} sec(s)!")
        print(f"Was the task cancelled? {long_task.cancelled()}")


if __name__ == "__main__":
    asyncio.run(main())
