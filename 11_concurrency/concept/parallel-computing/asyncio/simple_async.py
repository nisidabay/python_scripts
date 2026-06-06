#!/usr/bin/python3
"""
File: 
Author: RealPython.com
Email: 
Github: 
Description: Basic usage of a asyncio
"""

import asyncio
from async_utils import async_timed


async def count():
    print("One")
    await asyncio.sleep(1)
    print("Two")


@async_timed()
async def main():
    await asyncio.gather(*[count() for _ in range(3)])


if __name__ == "__main__":
    asyncio.run(main())
