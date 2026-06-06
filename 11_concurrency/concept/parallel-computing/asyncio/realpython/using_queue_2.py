#!/usr/bin/python3
"""
File: using_queue_2.py
Author: Vladyslav Krylasov
Email: 
Web: https://realpython.com/async-io-python/
Description: Producer-Consumer simulation using queues.
"""

import asyncio
import time
from typing import Tuple

INFO = '\033[34m{}\033[0m'
SUCCESS = '\033[32m{}\033[0m'
WARNING = '\033[33m{}\033[0m'


async def producer(q: asyncio.Queue, n: int) -> None:
    """Puts data to a queue.

    Args:
        q (asyncio.Queue): A queue object to store data and get it later on.
        n (int): A producer number.
    """

    data = (n, n * 2)
    print(INFO.format(f'Producer #{n} puts data <{data}> to the queue.'))
    await q.put(data)
    print(
        INFO.format(
            f'Queue was updated with data. The queue size is: {q.qsize()}'))
    print()


async def consumer(q: asyncio.Queue) -> Tuple[int, int]:
    """Gets data from a queue in FIFO (first in, first out) manner.

    Args:
        q (asyncio.Queue): A queue object to store data and get it later on.

    Returns:
        A producer number and its number multiplied value by a two.
    """

    print(INFO.format(f'The queue size is: {q.qsize()}'))
    n, value = await q.get()
    q.task_done()  # Indicate that a formerly enqueued task is complete.

    print(SUCCESS.format(f'Consumer #{n} got {value} of the producer #{n}.'))
    print()

    return n, value


async def main():
    queue = asyncio.Queue()

    # Create five producers tasks that will put data to the queue on launch.
    producers = [asyncio.create_task(producer(queue, n)) for n in range(5)]
    # Create ten consumers tasks that will get data from the queue.
    consumers = [asyncio.create_task(consumer(queue)) for _ in range(7)]

    # Return a future aggregating results from the given producers.
    await asyncio.gather(*producers)

    # Launch ten consumers tasks and wait until they all get data from the
    # queue. In reality, only five tasks will get data from the queue and the
    # rest of tasks will be cancelled.
    await queue.join()

    data = []
    for c in consumers:
        try:
            data.append(c.result())
        except asyncio.exceptions.InvalidStateError:
            print(
                WARNING.format(
                    f'{c.get_name()} is scheduled for cancellation.'))
            c.cancel()

    print(SUCCESS.format(f'Consumers collected the following data: {data}'))


if __name__ == '__main__':
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter() - start

    print(f'Took seconds: {end}')
