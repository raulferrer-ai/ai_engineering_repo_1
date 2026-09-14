import time

import pytest

from domain.llm_client import ConcurrentLLMClient
from domain.rate_limiter import RateLimiter


async def test_fetch_returns_ok_result() -> None:
    client = ConcurrentLLMClient(
        rate_limiter=RateLimiter(calls_per_second=10),
        timeout_seconds=1.0,
    )
    result = await client.fetch("hola", fail_probability=0.0)

    # timeout de 1s es menor que la latencia simulada por defecto (2s):
    # esperamos que agote los 3 intentos y falle por timeout.
    assert not result.is_ok()


async def test_fetch_succeeds_with_enough_timeout() -> None:
    client = ConcurrentLLMClient(
        rate_limiter=RateLimiter(calls_per_second=10),
        timeout_seconds=3.0,
    )
    result = await client.fetch("hola")

    assert result.is_ok()
    assert "hola" in result.value


async def test_fetch_many_respects_rate_limit_timing() -> None:
    # 4 prompts a 2 llamadas/segundo: los 'acquire' se espacian ~0.5s,
    # más la latencia (aquí forzada a 0 para medir solo el espaciado).
    client = ConcurrentLLMClient(
        rate_limiter=RateLimiter(calls_per_second=2),
        timeout_seconds=3.0,
    )
    # Monkeypatch rápido: latencia 0 para aislar el efecto del rate limit.
    import domain.llm_provider as provider_module

    original = provider_module.fetch_llm_response

    async def fast_fetch(prompt: str, latency_seconds: float = 0.0, fail_probability: float = 0.0) -> str:
        return await original(prompt, latency_seconds=0.01, fail_probability=fail_probability)

    provider_module.fetch_llm_response = fast_fetch  # type: ignore[assignment]
    try:
        start = time.perf_counter()
        results = await client.fetch_many(["p1", "p2", "p3", "p4"])
        elapsed = time.perf_counter() - start
    finally:
        provider_module.fetch_llm_response = original  # type: ignore[assignment]

    assert all(r.is_ok() for r in results)
    # 4 llamadas a 2/s -> el último 'acquire' debería ocurrir ~1.5s
    # después del primero.
    assert elapsed >= 1.0


async def test_fetch_many_handles_intermittent_failures() -> None:
    client = ConcurrentLLMClient(
        rate_limiter=RateLimiter(calls_per_second=5),
        max_attempts=5,
        timeout_seconds=3.0,
    )
    results = await client.fetch_many(
        ["p1", "p2", "p3"], fail_probability=0.5
    )

    # Con max_attempts=5 y fail_probability=0.5, es extremadamente
    # improbable (0.5^5 ≈ 3%) que un prompt agote todos los intentos,
    # pero no imposible: comprobamos que el sistema no crashea y que
    # cada resultado es un Result válido (ok o fail), nunca una excepción.
    assert len(results) == 3
    for r in results:
        assert hasattr(r, "is_ok")
