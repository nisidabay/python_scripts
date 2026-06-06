#!/usr/bin/python3
"""
File: using_queue_1.py
Author: Brad Solomon
Email: 
Web: https://realpython.com/async-io-python/
Description: Producer-Consumer simulation using queues.
"""
import asyncio
import os
import random
import time
from collections import namedtuple

Product = namedtuple("Product", "item time")


async def makeitem(size: int = 5) -> str:
    """ Makes a unique item identifier """

    return os.urandom(size).hex()


async def randsleep(caller=None) -> None:
    """ Seconds to sleep """

    secs_to_sleep = random.randint(0, 2)
    if caller:
        print(f"{caller} sleeping for {secs_to_sleep} seconds.")
    await asyncio.sleep(secs_to_sleep)


async def produce(product_qty: int, queue: asyncio.Queue) -> None:
    """ Puts random items in the queue """

    # for _ in it.repeat(None, product_qty):
    for number in range(product_qty + 1):
        await randsleep(caller=f"Producer-<{number}>")
        create_item = await makeitem()
        time_created = time.perf_counter()
        product = Product(create_item, time_created)
        await queue.put(product)
        print(f">>> Producer-<{number}> added <{product.item}> to queue.")


async def consume(consume_qty: int, queue: asyncio.Queue) -> None:
    """ Consume and item from the queue """

    for number in range(consume_qty + 1):
        await randsleep(caller=f"Consumer-<{number}>")
        item_from_queue = await queue.get()
        time_consumed = time.perf_counter()
        print(f"<<< Consumer-<{number}> consumed <{item_from_queue.item}>"
              f" in {time_consumed - item_from_queue.time:0.5f} seconds.")
        queue.task_done()


async def main(producer_number: int, consumer_number: int):
    """ Create and run tasks """

    queue = asyncio.Queue()
    producers = [
        asyncio.create_task(produce(n, queue)) for n in range(producer_number)
    ]
    consumers = [
        asyncio.create_task(consume(n, queue)) for n in range(consumer_number)
    ]

    await asyncio.gather(*producers)
    await queue.join()  # Implicitly awaits consumers, too

    for consumer in consumers:
        try:
            consumer.result()
        except asyncio.exceptions.InvalidStateError:
            consumer.cancel()


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main(5, 15))
    elapsed = time.perf_counter() - start
    print(f"[!] Program completed in {elapsed:0.5f} seconds.")
