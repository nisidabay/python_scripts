#!/usr/bin/python3
"""
File:asyncio_colorized_output.py 
Author: https://realpython.com/async-io-python/
Email: 
Github: 
Description: 
"""

import asyncio
import random

colors = (
    "\033[0m",  # Escape / Reset colors
    "\033[36m",  # Cyan
    "\033[91m",  # Pink
    "\033[35m",  # Fucsia
)


async def mk_random_color(color_idx: int, threshold: int) -> int:
    print(f"{colors[color_idx + 1]}Initiated mk_random_color({color_idx})")

    i = random.randint(0, 10)
    print(f"Threshold now is: {threshold}\n")
    while i <= threshold:
        print(
            colors[color_idx + 1] +
            f"mk_random_color({color_idx}) == {i} below threshold; retrying.")
        await asyncio.sleep(color_idx + 1)
        i = random.randint(0, 10)
    print(colors[color_idx + 1] +
          f"---> Finished: threshold: {threshold}, number: {i}\n" + colors[0])
    return i


async def main() -> list:
    res = await asyncio.gather(*(mk_random_color(i, 10 - i - 1)
                                 for i in range(3)))
    return res


if __name__ == "__main__":
    random.seed(444)
    r1, r2, r3 = tuple(asyncio.run(main()))
    print()
    print(f"r1: {r1}, r2: {r2}, r3: {r3}")
