import concurrent.futures
import time


def my_task(n: int) -> int:
    # Simulate a long-running task
    time.sleep(1)
    return n * 2


# Create a thread pool executor with 4 worker threads
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    # Launch a task and get a Future object
    future = executor.submit(my_task, 10)

    # Wait for the task to complete
    result = future.result()
    if future.done():

        # Print the result
        print(result)  # Output: 20
