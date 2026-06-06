#!/usr/bin/python3
import asyncio
from async_utils import delay, async_timed
from typing import AsyncGenerator


async def aiterator() -> AsyncGenerator:
    for i in range(5):
        await delay(i)
        yield i
        print("doing somethin else")


@async_timed()
async def main() -> None:
    async for x in aiterator():
        print(x)


if __name__ == "__main__":
    asyncio.run(main())
