"""Decorators reutilizables para instrumentar funciones del sistema."""

import time
from functools import wraps
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def timing(fn: Callable[P, R]) -> Callable[P, R]:
    """Mide e imprime el tiempo de ejecución, sin alterar resultado
    ni firma de la función decorada."""

    @wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[timing] {fn.__name__} tardó {elapsed:.6f}s")
        return result

    return wrapper
