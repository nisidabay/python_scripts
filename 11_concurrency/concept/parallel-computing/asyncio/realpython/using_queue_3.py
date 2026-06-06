#!/usr/bin/python3
"""
File: using_queue_1.py
Author: Vladyslav Krylasov
Email: 
Web: https://realpython.com/async-io-python/
Description: Producer-Consumer simulation using queues.
"""
import asyncio
import time


async def producer(q: asyncio.Queue, n: int) -> None:
    value = n * 2
    await q.put((n, value))
    print(f"Producers puts item: <{n}> with value: <{value}> to the queue")


async def main():
    queue = asyncio.Queue()
    tasks = [asyncio.create_task(producer(queue, n)) for n in range(5)]

    await asyncio.gather(*tasks)

    while not queue.empty():
        print(f"Queue size is: <{queue.qsize()}>")
        n, value = await queue.get()
        queue.task_done()
        print(f"Producer gets item: #{n} with Value: {value} from the queue")

    await queue.join()


if __name__ == '__main__':
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter() - start
    print(f'Took seconds: {end}')
