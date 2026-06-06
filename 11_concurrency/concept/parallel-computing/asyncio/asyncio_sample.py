#!/usr/bin/python3
import asyncio
from async_utils import delay


async def talk(name, script):

    print("Enters", end=" ")
    for act in script:
        print(f"{name}: {act}")
        await delay(2)
    print(f"{name} exit...\n")


async def main():
    tasks = [
        asyncio.create_task(
            talk("Ross", ["I am good", "I am better than you", "absolutely"])),
        asyncio.create_task(
            talk("Mark", [
                "Me too!\n",
                "Really?\n",
                "What a stupid guy!\n",
                "I am done\n",
            ])),
    ]

    for t in tasks:
        await t
    print("\nThe End")


if __name__ == "__main__":
    asyncio.run(main())
