#!/usr/bin/python3
import asyncio


class OddCounter:
    def __init__(self, end_range):
        self.end = end_range
        self.start = -1

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.start >= self.end - 1:
            raise StopAsyncIteration
        self.start += 2
        return self.start


async def main():
    async for c in OddCounter(100):
        print(c)


if __name__ == "__main__":
    asyncio.run(main())
