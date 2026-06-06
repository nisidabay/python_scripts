#!/usr/bin/python3
""" Delay the execution of a coroutine """
import asyncio


async def delay(delay_seconds: int | float) -> None:
    print(f"sleeping for {delay_seconds} seconds(s)")
    await asyncio.sleep(delay_seconds)
    print(f"finished sleeping for {delay_seconds} seconds(s)")
