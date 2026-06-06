#!/usr/bin/python3
"""
File: aiohttp_example.py 
Author: RealPython.com
Email: 
Github: 
Description: Show asynchronous network connections
"Get 3 random numbers between 0 and 65535
"""

import asyncio
import json
import time
import aiohttp
from typing import Any


async def worker(name: str, numbers: int, session: Any) -> str:
    """ Create the worker to fetch the data """

    print(f"worker-{name}")
    url = f"https://qrng.anu.edu.au/API/jsonI.php?length={numbers}&type=uint16"
    response = await session.request(method="GET", url=url)
    value = await response.text()
    value = json.loads(value)
    return value['data']


async def main() -> None:
    """ Create the connection  """

    async with aiohttp.ClientSession() as session:
        response = await worker("dummy", 3, session)
        print(f"response: {response}")


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    elapse = time.perf_counter() - start
    print(f"Excuted in {elapse:.4f} sec(s)")
