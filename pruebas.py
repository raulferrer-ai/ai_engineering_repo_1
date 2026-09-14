import asyncio
import time
from contextlib import asynccontextmanager


@asynccontextmanager
async def timed_block(label: str):
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"{label}: {elapsed:.2f} segundos")


async def fetch_llm_response(prompt: str) -> str:
    print(f"Llamando al modelo con: {prompt}")
    await asyncio.sleep(2)
    return f"Respuesta simulada para: {prompt}"


class RateLimiter:
    def __init__(self, calls_per_second: float) -> None:
        self._interval = 1.0 / calls_per_second
        self._lock = asyncio.Lock()
        self._last_call = 0.0

    async def acquire(self) -> None:
        async with self._lock:
            now = asyncio.get_event_loop().time()
            wait = self._last_call + self._interval - now

            if wait > 0:
                await asyncio.sleep(wait)

            self._last_call = asyncio.get_event_loop().time()


async def fetch_with_rate_limit(
    prompt: str,
    rate_limiter: RateLimiter,
) -> str:
    await rate_limiter.acquire()
    return await fetch_llm_response(prompt)


async def main():
    prompts = [
        "Prompt 1",
        "Prompt 2",
        "Prompt 3",
        "Prompt 4",
        "Prompt 5",
        "Prompt 6",
    ]

    rate_limiter = RateLimiter(calls_per_second=2)

    async with timed_block("Tiempo total"):
        responses = await asyncio.gather(
            *(
                fetch_with_rate_limit(prompt, rate_limiter)
                for prompt in prompts
            )
        )

    print("\nResultados:")
    for response in responses:
        print(response)


if __name__ == "__main__":
    asyncio.run(main())
