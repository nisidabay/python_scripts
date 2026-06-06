def perf_timer(orig_func):
    """ Decorator for timing the executable time of a function """

    @wraps(orig_func)
    def wrapper(*args, **kwargs):

        print(f"[+] Proccessing. Wait to finish...")

        t1 = time.perf_counter()
        result = orig_func(*args, **kwargs)
        t2 = time.perf_counter() - t1

        tt = t2 - t1
        print(type(tt))

        print(f"[+] Proccess took {tt}")

        return result

    return wrapper