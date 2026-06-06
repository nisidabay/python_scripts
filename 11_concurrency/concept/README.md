# Concurrency — Threads, asyncio, multiprocessing, and concurrent.futures

## Quick Start
```bash
# Threads: Basic Thread creation, subclassing, race conditions, locks
python parallel-computing/threads/Thread-1.py
python parallel-computing/threads/Thread-2.py
python parallel-computing/threads/race_condition.py
python parallel-computing/threads/avoid_race_condition_1.py
python parallel-computing/threads/subclassing_thread_1.py
python parallel-computing/threads/threadpoolexecutor-1.py

# Multiprocessing: Process pools, parallel for-loops
python parallel-computing/multiprocessing/mutiprocessing-1.py

# concurrent.futures: Modern high-level executor interface
python parallel-computing/concurrent-futures/example-1.py

# asyncio: coroutines, tasks, gather, cancellation, queues, aiohttp
python parallel-computing/asyncio/asyncio_basic.py
python parallel-computing/asyncio/create_task.py
python parallel-computing/asyncio/asyncio_gather.py
python parallel-computing/asyncio/asyncio_tasks.py
python parallel-computing/asyncio/multiple_tasks.py
python parallel-computing/asyncio/realpython/aiohttp_example.py
```

## Learning Path
| File | Concept | Key Pattern |
|------|---------|-------------|
| `threads/Thread-1.py` | Basic `Thread(target=fn, args=…)`, start all, join all | List comprehension threads → `.start()` → `.join()` loop |
| `threads/Thread-2.py` | OOP wrapper: `ParallelThread` class encapsulating create/start/wait | Class wraps thread lifecycle, `@staticmethod` task |
| `threads/race_condition.py` | Unprotected shared state across threads | Demonstrates data corruption without synchronization |
| `threads/avoid_race_condition_1.py` | Lock-based mutual exclusion | `threading.Lock().acquire()/.release()` critical section |
| `threads/subclassing_thread_1.py` | Extending `Thread` class, overriding `run()` | OOP thread model with custom `run()` method |
| `threads/threadpoolexecutor-1.py` | `multiprocessing.pool.ThreadPool` with `pool.map()` | Context-managed pool, `pool.map(fn, iterable)` |
| `multiprocessing/mutiprocessing-1.py` | `ThreadPool` for CPU-bound parallelism | `multiprocessing.pool.ThreadPool` context manager |
| `concurrent-futures/example-1.py` | `ThreadPoolExecutor.submit()` → `Future.result()` | Modern high-level API, `with ThreadPoolExecutor(max_workers=4)` |
| `asyncio/asyncio_basic.py` | Coroutines, `async def`, `await`, nested `create_task` | `asyncio.run(main())`, `asyncio.create_task(subtask())` |
| `asyncio/create_task.py` | Task creation and awaiting | `asyncio.create_task(delay(3))` → `await task` |
| `asyncio/asyncio_gather.py` | Concurrent coroutines with `gather` | `await asyncio.gather(coro1(), coro2())` |
| `asyncio/asyncio_tasks.py` | Task groups, concurrent execution | `asyncio.TaskGroup` or `asyncio.create_task` for parallelism |
| `asyncio/realpython/aiohttp_example.py` | Async HTTP client with aiohttp | `async with aiohttp.ClientSession()` |

> **Full path note:** All files live under `parallel-computing/` subdirectory. There are 50+ files total — the above are representative highlights.

## Common Patterns
```python
# Threads: parallel execution
from threading import Thread
threads = [Thread(target=worker, args=(i,)) for i in range(10)]
for t in threads: t.start()
for t in threads: t.join()

# Thread safety with Lock
from threading import Lock
lock = Lock()
def safe_update():
    with lock:
        shared_counter += 1

# concurrent.futures: modern executor pattern
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=4) as executor:
    future = executor.submit(my_task, 10)
    result = future.result()

# asyncio: coroutines and tasks
import asyncio
async def main():
    tasks = [asyncio.create_task(delay(i)) for i in [3, 2, 1]]
    results = await asyncio.gather(*tasks)
asyncio.run(main())
```

## Now Build Your Own
**Challenge:** Write an async URL fetcher that downloads 10 URLs concurrently. Time how long it takes with `asyncio.gather` vs a sequential loop. Print each result's first 100 characters and the total elapsed time. Add a 5-second timeout per request using `asyncio.wait_for`.
