"""Lógica de reintentos, combinando Result[T] con una excepción para
el caso excepcional (agotar todos los intentos).
"""

from typing import Callable, TypeVar

from domain.exceptions import RetryExhaustedError
from domain.result import Result

T = TypeVar("T")


def run_with_retry(fn: Callable[[], T], max_attempts: int = 3) -> Result[T]:
    """Reintenta `fn` hasta max_attempts veces.

    Nota de diseño (deliberada, revisar en Q3 - Reliability):
    la firma promete Result[T], pero además puede lanzar
    RetryExhaustedError cuando se agotan los intentos. Es un contrato
    mixto: úsalo sabiendo que quien llame debe manejar ambos casos.
    """
    last_error: Exception | None = None

    for _attempt in range(max_attempts):
        try:
            return Result.ok(fn())
        except Exception as e:  # noqa: BLE001 - punto de frontera intencional
            last_error = e

    assert last_error is not None
    raise RetryExhaustedError(attempts=max_attempts, last_error=last_error) from last_error
