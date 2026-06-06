#!/usr/bin/python3
import asyncio
from async_utils import delay, async_timed


@async_timed()
async def main() -> None:
    sleep_for_three = asyncio.create_task(delay(3))
    sleep_again = asyncio.create_task(delay(2))
    sleep_once_more = asyncio.create_task(delay(1))

    await sleep_for_three
    await sleep_again
    await sleep_once_more


if __name__ == "__main__":
    asyncio.run(main())
