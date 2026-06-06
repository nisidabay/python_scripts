#!/usr/bin/env python3
"""Concurrency exercises: threading, futures, asyncio, multiprocessing, producer-consumer."""

import asyncio
import concurrent.futures
import math
import multiprocessing
import queue
import threading
import time
from typing import Any


# ═══════════════════════════════════════════════════════════════════════════════
# Module-level definitions: functions must be picklable for multiprocessing
# ═══════════════════════════════════════════════════════════════════════════════

def fetch_url(url: str) -> tuple[str, int]:
    """Simulate a network fetch with a delay. Returns (url, status_code)."""
    time.sleep(0.2)  # simulate network latency
    return (url, 200)  # pretend all succeed


def api_call(endpoint: str) -> dict[str, Any]:
    """Simulate an API call returning JSON."""
    time.sleep(0.15)
    return {"endpoint": endpoint, "data": f"result for {endpoint}", "status": "ok"}


async def async_fetch(item_id: int) -> dict[str, Any]:
    """Coroutine that simulates an async I/O operation."""
    await asyncio.sleep(0.15)  # non-blocking sleep — yield control
    return {"id": item_id, "value": item_id * 10}


async def run_async_gather():
    """Gather multiple coroutines and run them concurrently."""
    tasks = [async_fetch(i) for i in range(5)]
    return await asyncio.gather(*tasks)


def is_prime(n: int) -> bool:
    """CPU-bound: check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(math.isqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def find_primes_in_range(start: int, end: int) -> list[int]:
    """Find all primes in [start, end). CPU-bound workload."""
    return [n for n in range(start, end) if is_prime(n)]


def producer(q: queue.Queue, items: list[int], done_signal: object):
    """Produce items into the queue, then signal completion."""
    for item in items:
        time.sleep(0.05)
        q.put(item)
        print(f"  [Producer] put {item}")
    q.put(done_signal)


def consumer(q: queue.Queue, done_signal: object) -> list[int]:
    """Consume items from the queue until sentinel is received."""
    consumed = []
    while True:
        item = q.get()
        if item is done_signal:
            q.task_done()
            break
        consumed.append(item)
        print(f"  [Consumer] got {item}")
        q.task_done()
        time.sleep(0.08)
    return consumed


# ═══════════════════════════════════════════════════════════════════════════════
# Main: all exercises run from here (guarded by __name__ == "__main__")
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    # --- Exercise 1: threading ---
    urls = [
        "https://api.example.com/users",
        "https://api.example.com/orders",
        "https://api.example.com/products",
    ]

    threads = []
    results: list[tuple[str, int]] = []

    for url in urls:
        t = threading.Thread(
            target=lambda u=url: results.append(fetch_url(u)),
            daemon=True,
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("Exercise 1 — Threaded URL fetches:")
    for url, status in results:
        print(f"  {url} → {status}")
    print("---")

    # --- Exercise 2: ThreadPoolExecutor ---
    endpoints = ["/users/1", "/users/2", "/users/3", "/orders/99"]

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(api_call, ep): ep for ep in endpoints}
        results2 = []
        for future in concurrent.futures.as_completed(futures):
            results2.append(future.result())

    print("Exercise 2 — ThreadPoolExecutor API calls:")
    for r in sorted(results2, key=lambda x: x["endpoint"]):
        print(f"  {r['endpoint']} → {r['data']}")
    print("---")

    # --- Exercise 3: asyncio ---
    results3 = asyncio.run(run_async_gather())

    print("Exercise 3 — asyncio.gather:")
    for r in results3:
        print(f"  id={r['id']}, value={r['value']}")
    print("---")

    # --- Exercise 4: multiprocessing ---
    # Must use 'spawn' or guard with __name__; 'fork' would work but is unsafe with threads
    ctx = multiprocessing.get_context("spawn")
    with ctx.Pool(processes=4) as pool:
        ranges = [(1, 250), (250, 500), (500, 750), (750, 1000)]
        chunk_results = pool.starmap(find_primes_in_range, ranges)

    all_primes = [p for chunk in chunk_results for p in chunk]
    print(f"Exercise 4 — Multiprocessing prime count (1–999): {len(all_primes)} primes")
    print(f"  Sample: {all_primes[:10]}...{all_primes[-5:]}")
    print("---")

    # --- BONUS: Producer-consumer ---
    q: queue.Queue = queue.Queue()
    DONE = object()
    result_container: list[list[int]] = []

    def consumer_wrapper():
        result_container.append(consumer(q, DONE))

    cons_thread = threading.Thread(target=consumer_wrapper)
    prod_thread = threading.Thread(target=producer, args=(q, [10, 20, 30, 40, 50], DONE))

    prod_thread.start()
    cons_thread.start()
    prod_thread.join()
    cons_thread.join()

    print(f"BONUS — Producer-consumer consumed: {result_container[0]}")
    assert result_container[0] == [10, 20, 30, 40, 50]
    print("---")

    print("All concurrency exercises passed.")


if __name__ == "__main__":
    main()
