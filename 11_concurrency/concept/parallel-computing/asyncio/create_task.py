#!/usr/bin/python3
import asyncio
from async_utils import delay, async_timed


@async_timed()
async def main() -> None:
    sleep_for_three = asyncio.create_task(delay(3))
    result = await sleep_for_three
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
