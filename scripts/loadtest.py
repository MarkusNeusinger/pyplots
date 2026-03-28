"""
Load test for Cloud Run services (pyplots frontend + backend).
Tests increasing concurrency levels to find the performance breaking point.

Usage:
    uv run python scripts/loadtest.py frontend
    uv run python scripts/loadtest.py backend
    uv run python scripts/loadtest.py all
"""

import asyncio
import statistics
import sys
import time

import httpx

CONCURRENCY_LEVELS = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
DURATION_PER_LEVEL = 30  # seconds
WARMUP_REQUESTS = 5
DEGRADATION_STREAK_LIMIT = 3  # abort after N consecutive degraded levels

TARGETS = {
    "frontend": {
        "name": "Frontend (pyplots.ai)",
        "urls": ["https://pyplots.ai/"],
    },
    "backend": {
        "name": "Backend (api.pyplots.ai)",
        "urls": [
            "https://api.pyplots.ai/specs",
            "https://api.pyplots.ai/stats",
        ],
    },
}


async def make_request(client: httpx.AsyncClient, url: str) -> tuple[float, int]:
    """Make a single request, return (latency_ms, status_code)."""
    start = time.monotonic()
    try:
        resp = await client.get(url, timeout=30.0)
        latency = (time.monotonic() - start) * 1000
        return latency, resp.status_code
    except Exception:
        latency = (time.monotonic() - start) * 1000
        return latency, 0


async def run_level(
    client: httpx.AsyncClient, urls: list[str], concurrency: int, duration: float
) -> dict:
    """Run load at a given concurrency level for `duration` seconds."""
    latencies: list[float] = []
    errors = 0
    total = 0
    url_idx = 0
    start = time.monotonic()

    async def worker():
        nonlocal errors, total, url_idx
        while time.monotonic() - start < duration:
            url = urls[url_idx % len(urls)]
            url_idx += 1
            latency, status = await make_request(client, url)
            total += 1
            latencies.append(latency)
            if status < 200 or status >= 400:
                errors += 1

    workers = [asyncio.create_task(worker()) for _ in range(concurrency)]
    await asyncio.gather(*workers)
    elapsed = time.monotonic() - start

    if not latencies:
        return {"concurrency": concurrency, "error": "no responses"}

    latencies.sort()
    return {
        "concurrency": concurrency,
        "requests": total,
        "rps": round(total / elapsed, 1),
        "p50": round(statistics.median(latencies), 1),
        "p95": round(latencies[int(len(latencies) * 0.95)], 1),
        "p99": round(latencies[int(len(latencies) * 0.99)], 1),
        "max": round(max(latencies), 1),
        "errors": errors,
        "error_rate": round(errors / total * 100, 1) if total else 0,
    }


def is_degraded(result: dict, baseline_p95: float | None) -> bool:
    """Check if this level shows significant degradation vs baseline."""
    if "error" in result:
        return True
    if result["error_rate"] > 5:
        return True
    if baseline_p95 and result["p95"] > baseline_p95 * 3:
        return True
    return False


def print_results(name: str, results: list[dict]):
    print(f"\n{'=' * 90}")
    print(f"  {name}")
    print(f"{'=' * 90}")
    header = f"{'Conc':>6} {'Reqs':>7} {'RPS':>8} {'p50ms':>8} {'p95ms':>8} {'p99ms':>8} {'MaxMs':>8} {'Errs':>6} {'Err%':>6}"
    print(header)
    print("-" * 90)

    prev_p95 = None
    for r in results:
        if "error" in r:
            print(f"{r['concurrency']:>6}  ERROR: {r['error']}")
            continue

        flag = ""
        if prev_p95 and r["p95"] > prev_p95 * 2:
            flag = " << DEGRADATION"
        if r["error_rate"] > 5:
            flag = " << HIGH ERRORS"

        print(
            f"{r['concurrency']:>6} {r['requests']:>7} {r['rps']:>8} "
            f"{r['p50']:>8} {r['p95']:>8} {r['p99']:>8} {r['max']:>8} "
            f"{r['errors']:>6} {r['error_rate']:>5}%{flag}"
        )
        prev_p95 = r["p95"]

    print()


async def warmup(client: httpx.AsyncClient, urls: list[str]):
    """Send a few warmup requests to ensure caches are primed."""
    print("  Warming up...", end="", flush=True)
    for _ in range(WARMUP_REQUESTS):
        for url in urls:
            await make_request(client, url)
    print(" done")


async def test_target(target_key: str):
    target = TARGETS[target_key]
    print(f"\nTesting: {target['name']}")
    print(f"Endpoints: {', '.join(target['urls'])}")
    print(f"Levels: {CONCURRENCY_LEVELS}, {DURATION_PER_LEVEL}s each")
    print(f"Early abort: after {DEGRADATION_STREAK_LIMIT} consecutive degraded levels")

    results = []
    baseline_p95 = None
    degradation_streak = 0

    async with httpx.AsyncClient(follow_redirects=True) as client:
        await warmup(client, target["urls"])

        for level in CONCURRENCY_LEVELS:
            print(f"  Concurrency {level:>3} ({DURATION_PER_LEVEL}s)...", end="", flush=True)
            result = await run_level(client, target["urls"], level, DURATION_PER_LEVEL)
            results.append(result)
            rps = result.get("rps", "?")
            p95 = result.get("p95", "?")
            print(f" {rps} rps, p95={p95}ms")

            # Track baseline from first stable level
            if baseline_p95 is None and not is_degraded(result, None):
                baseline_p95 = result.get("p95")

            # Check for degradation streak
            if is_degraded(result, baseline_p95):
                degradation_streak += 1
                if degradation_streak >= DEGRADATION_STREAK_LIMIT:
                    print(f"\n  EARLY ABORT: {DEGRADATION_STREAK_LIMIT} consecutive degraded levels detected")
                    break
            else:
                degradation_streak = 0

    print_results(target["name"], results)
    return results


async def main():
    targets = sys.argv[1:] if len(sys.argv) > 1 else ["all"]

    if "all" in targets:
        targets = ["frontend", "backend"]

    for t in targets:
        if t not in TARGETS:
            print(f"Unknown target: {t}. Choose from: {', '.join(TARGETS.keys())}, all")
            sys.exit(1)

    for t in targets:
        await test_target(t)


if __name__ == "__main__":
    asyncio.run(main())
