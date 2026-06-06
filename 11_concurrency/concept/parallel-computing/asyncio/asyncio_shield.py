#!/usr/bin/python3
""" To inform the user that a coroutine is still running without cancelling it"""
import asyncio
from async_utils import delay, async_timed


@async_timed()
async def main():
    threshold = 7
    wait_for = 10

    long_task = asyncio.create_task(delay(wait_for))
    try:
        await asyncio.wait_for(asyncio.shield(long_task), timeout=threshold)
    except asyncio.exceptions.TimeoutError:
        print(
            f"Task takes longer than {wait_for} sec(s), it will finish soon!")
        await long_task


if __name__ == "__main__":
    asyncio.run(main())
