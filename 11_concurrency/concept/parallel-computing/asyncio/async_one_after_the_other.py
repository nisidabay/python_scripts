#!/usr/bin/python3

# Ways to run coroutines
# With await although asyncronously, the coroutines are running one after the
# other

# Use asyncio.run()

#--------------------------------------
# loop.run_until_complete() DEPRECATED
#--------------------------------------
import asyncio
from async_utils import async_timed, delay


async def waiter() -> None:
    await cook("pasta", 0.8)
    await cook("Caesar Saladad", 0.3)
    await cook("Lamb Chops", 0.16)


@async_timed()
async def cook(order: str, time_to_prepare: float) -> None:
    print(f"Getting {order} order")
    await delay(time_to_prepare)
    print(f"{order} ready!")


if __name__ == "__main__":
    asyncio.run(waiter())
    print("""\n
    There's no effect of asyncio here.
    Every coroutine is running sequentially""")
