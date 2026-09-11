"""Result[T]: modela una operación que puede tener éxito o fallar,
sin recurrir a excepciones para el flujo esperado de negocio.

Equivalente conceptual a Result<T, Error> en Swift.
"""

from typing import Generic, TypeVar

T = TypeVar("T")


class Result(Generic[T]):
    def __init__(self, value: T | None, error: str | None) -> None:
        self.value = value
        self.error = error

    def is_ok(self) -> bool:
        """True si la operación fue exitosa (no hay error)."""
        return self.error is None

    @classmethod
    def ok(cls, value: T) -> "Result[T]":
        return cls(value=value, error=None)

    @classmethod
    def fail(cls, error: str) -> "Result[T]":
        return cls(value=None, error=error)

    def __repr__(self) -> str:
        if self.is_ok():
            return f"Result.ok({self.value!r})"
        return f"Result.fail({self.error!r})"
