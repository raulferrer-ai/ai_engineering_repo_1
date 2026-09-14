"""Cliente concurrente para llamadas a un LLM.

Tubería por cada intento individual:

    rate_limiter.acquire() -> timeout -> llamada real -> Result

Decisión de diseño (Opción B, discutida en la Semana 2): el retry
envuelve TODO lo anterior, incluido el rate limit. Cada reintento es
una petición de red real y debe pasar por el rate limiter de forma
independiente -si el rate limit envolviera al retry, un solo "turno"
del limitador podría esconder 2-3 peticiones reales, rompiendo la
garantía de peticiones/segundo frente al proveedor real.
"""

import asyncio

from domain.llm_provider import fetch_llm_response
from domain.rate_limiter import RateLimiter
from domain.result import Result


class ConcurrentLLMClient:
    def __init__(
        self,
        rate_limiter: RateLimiter,
        max_attempts: int = 3,
        timeout_seconds: float = 5.0,
    ) -> None:
        self._rate_limiter = rate_limiter
        self._max_attempts = max_attempts
        self._timeout_seconds = timeout_seconds

    async def fetch(self, prompt: str, fail_probability: float = 0.0) -> Result[str]:
        """Ejecuta un único prompt a través de la tubería completa."""
        last_error: Exception | None = None

        for _attempt in range(self._max_attempts):
            await self._rate_limiter.acquire()

            try:
                async with asyncio.timeout(self._timeout_seconds):
                    response = await fetch_llm_response(
                        prompt, fail_probability=fail_probability
                    )
                    return Result.ok(response)
            except TimeoutError as e:
                last_error = e
            except Exception as e:  # noqa: BLE001 - frontera intencional
                last_error = e

        return Result.fail(
            f"Fallaron los {self._max_attempts} intentos. Último error: {last_error}"
        )

    async def fetch_many(
        self, prompts: list[str], fail_probability: float = 0.0
    ) -> list[Result[str]]:
        """Ejecuta fetch() para todos los prompts de forma concurrente."""
        return await asyncio.gather(
            *(self.fetch(p, fail_probability=fail_probability) for p in prompts)
        )
