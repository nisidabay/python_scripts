#!/usr/bin/python3
import asyncio
from async_utils import delay, async_timed


async def add_one(number: int) -> int:
    return number + 1


async def hello_world_message() -> str:
    await delay(1)
    return "Hello world"


@async_timed()
async def main() -> None:
    one_plus_one = asyncio.create_task(add_one(1))
    message = asyncio.create_task(hello_world_message())
    o = await one_plus_one
    m = await message
    print(o)
    print(m)


if __name__ == "__main__":
    asyncio.run(main())
