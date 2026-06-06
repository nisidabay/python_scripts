#!/usr/bin/python3
import asyncio
import timeit


async def operate(time: int, result: int):
    print(f"Spending {time} seconds doing operations ...")
    await asyncio.sleep(time)
    print(f"Operations done after {time} seconds")
    return result


async def amain():
    x, y = await asyncio.gather(operate(5, 42), operate(2, 23))
    print(f"Got {x=}, {y=}")
    assert x == 42
    assert y == 23


if __name__ == "__main__":
    t = timeit.timeit("asyncio.run(amain())", globals=globals(), number=1)
    print(f"{t=}")
