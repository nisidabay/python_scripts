#!/usr/bin/env python3
"""Concurrent URL fetcher — downloads multiple URLs with thread pool, asyncio, or multiprocessing."""

import argparse
import concurrent.futures
import multiprocessing
import os
import sys
import time
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse


@dataclass
class FetchResult:
    url: str
    status: Optional[int] = None
    size: int = 0
    elapsed: float = 0.0
    error: Optional[str] = None


def fetch_one(url: str, timeout: float = 30.0) -> FetchResult:
    """Fetch a single URL, return result."""
    start = time.monotonic()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "fetcher/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read()
            elapsed = time.monotonic() - start
            return FetchResult(
                url=url,
                status=resp.status,
                size=len(data),
                elapsed=elapsed,
            )
    except Exception as exc:
        elapsed = time.monotonic() - start
        return FetchResult(url=url, elapsed=elapsed, error=str(exc))


def mode_threads(urls: list[str], workers: int, timeout: float) -> list[FetchResult]:
    """Fetch using ThreadPoolExecutor."""
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {ex.submit(fetch_one, url, timeout): url for url in urls}
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
    return results


def mode_processes(urls: list[str], workers: int, timeout: float) -> list[FetchResult]:
    """Fetch using ProcessPoolExecutor."""
    results = []
    # Use a pool with spawn context to avoid pickling issues
    ctx = multiprocessing.get_context("spawn")
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers, mp_context=ctx) as ex:
        futures = {ex.submit(fetch_one, url, timeout): url for url in urls}
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
    return results


def mode_sequential(urls: list[str], timeout: float) -> list[FetchResult]:
    """Fetch one at a time."""
    return [fetch_one(url, timeout) for url in urls]


def report(results: list[FetchResult], total_elapsed: float) -> None:
    success = [r for r in results if r.error is None]
    failed = [r for r in results if r.error is not None]

    total_bytes = sum(r.size for r in success)

    print(f"\n{'='*60}")
    print(f"Results: {len(success)} success, {len(failed)} failed")
    print(f"Total time: {total_elapsed:.2f}s")
    print(f"Total downloaded: {total_bytes:,} bytes")
    if success:
        avg = sum(r.elapsed for r in success) / len(success)
        print(f"Average request: {avg:.2f}s")
    print(f"{'='*60}")

    if success:
        print("\nSuccessful:")
        for r in sorted(success, key=lambda x: x.elapsed):
            print(f"  [{r.status}] {r.elapsed:.2f}s {r.size:>10,}B  {r.url}")

    if failed:
        print("\nFailed:")
        for r in failed:
            print(f"  ERROR  {r.elapsed:.2f}s  {r.url}")
            print(f"         {r.error}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Concurrent URL fetcher — download multiple URLs with threads, asyncio, or processes.",
    )
    parser.add_argument(
        "urls", nargs="+", help="URLs to fetch",
    )
    parser.add_argument(
        "--mode", choices=["sequential", "threads", "processes"],
        default="threads",
        help="Concurrency mode (default: threads)",
    )
    parser.add_argument(
        "--workers", type=int, default=5,
        help="Number of workers for threads/processes (default: 5)",
    )
    parser.add_argument(
        "--timeout", type=float, default=30.0,
        help="Request timeout in seconds (default: 30)",
    )
    parser.add_argument(
        "--output-dir", default=None,
        help="Save downloaded content to this directory",
    )

    args = parser.parse_args()

    print(f"Fetching {len(args.urls)} URL(s) with mode={args.mode}, workers={args.workers}")

    start = time.monotonic()

    if args.mode == "sequential":
        results = mode_sequential(args.urls, args.timeout)
    elif args.mode == "threads":
        results = mode_threads(args.urls, args.workers, args.timeout)
    elif args.mode == "processes":
        results = mode_processes(args.urls, args.workers, args.timeout)
    else:
        print(f"Unknown mode: {args.mode}", file=sys.stderr)
        return 1

    total_elapsed = time.monotonic() - start
    report(results, total_elapsed)

    # Save if requested
    if args.output_dir:
        out = Path(args.output_dir)
        out.mkdir(parents=True, exist_ok=True)
        for r in results:
            if r.error is None and r.size > 0:
                # Re-fetch synchronously to save (we discarded the data)
                try:
                    res2 = fetch_one(r.url, args.timeout)
                    if res2.error is None:
                        parsed = urlparse(r.url)
                        fname = Path(parsed.path).name or "index.html"
                        fpath = out / fname
                        # Actually fetch and save
                        with urllib.request.urlopen(r.url, timeout=args.timeout) as resp:
                            data = resp.read()
                            fpath.write_bytes(data)
                        print(f"Saved: {fpath}")
                except Exception as exc:
                    print(f"Save failed for {r.url}: {exc}", file=sys.stderr)

    return 0 if all(r.error is None for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
