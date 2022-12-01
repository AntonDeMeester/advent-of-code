import time
from typing import Callable


def run_and_benchmark(solution: Callable[[], int]):
    start = time.time()
    result = solution()
    duration = time.time() - start
    print(f"The solution is {result} and it took {_format_time(duration)}")


def _format_time(duration: float) -> str:
    if duration < 1e-3:
        return f"{duration * 10e6:.3f}ns"
    elif duration < 1:
        return f"{duration * 10e3:.3f}ms"
    elif duration < 60:
        return f"{duration:.3f}s"
    else:
        return f"{duration // 60}min {duration % 60:.3f}s"
