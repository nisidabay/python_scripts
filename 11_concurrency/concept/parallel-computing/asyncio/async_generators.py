#!/usr/bin/python3

import asyncio
from typing import AsyncGenerator


async def async_range(n: int) -> AsyncGenerator:
    for i in range(n):
        await asyncio.sleep(1)
        yield i


async def main() -> None:
    async for i in async_range(10):
        print(i)
        print("Doing other thing")


if __name__ == "__main__":
    asyncio.run(main())
