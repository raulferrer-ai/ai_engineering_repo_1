"""Lógica de reintentos síncrona, combinando Result[T] con una
excepción para el caso excepcional (agotar todos los intentos)."""

from typing import Callable, TypeVar

from domain.exceptions import RetryExhaustedError
from domain.result import Result

T = TypeVar("T")


def run_with_retry(fn: Callable[[], T], max_attempts: int = 3) -> Result[T]:
    last_error: Exception | None = None

    for _attempt in range(max_attempts):
        try:
            return Result.ok(fn())
        except Exception as e:  # noqa: BLE001 - frontera intencional
            last_error = e

    assert last_error is not None
    raise RetryExhaustedError(attempts=max_attempts, last_error=last_error) from last_error
