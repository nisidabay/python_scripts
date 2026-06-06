#!/usr/bin/python3
import asyncio


async def get_value_for_key(keys, key):
    return keys.get(key)


class KeyTaker:
    def __init__(self, keys):
        self.keys = keys

    def __aiter__(self):
        self.iter_keys = iter(self.keys)
        return self

    async def __anext__(self):
        try:
            k = next(self.iter_keys)
        except StopIteration as e:
            raise StopAsyncIteration from e
        value = await get_value_for_key(self.keys, k)
        return value

    def __len__(self):
        return len(self.keys)


async def main():
    keys = {
        "key1": 1234,
        "key2": 2345,
        "key3": 3456,
        "key4": 4567,
        "key5": 5678
    }
    async for c in KeyTaker(keys):
        await asyncio.sleep(0.1)
        print(c)


if __name__ == "__main__":
    asyncio.run(main())
