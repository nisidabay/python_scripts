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
    message = await hello_world_message()
    one_plus_one = await add_one(1)
    print(one_plus_one)
    print(message)


if __name__ == "__main__":
    asyncio.run(main())
