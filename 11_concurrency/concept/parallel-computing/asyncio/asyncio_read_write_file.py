#!/usr/bin/python3
""" Reading and writing file using asyncio """

import asyncio


async def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()


async def write_file(filename, content):
    with open(filename, 'w') as f:
        f.write(content)


async def main():
    content = await read_file('my_file.txt')
    await write_file('copy.txt', content)


if __name__ == "__main__":
    asyncio.run(main())
