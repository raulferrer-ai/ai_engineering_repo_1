"""Context managers del dominio."""

import time
from collections.abc import Iterator
from contextlib import contextmanager


@contextmanager
def timed_block(name: str) -> Iterator[None]:
    """Imprime cuánto tiempo pasó dentro del bloque `with`,
    incluso si el bloque lanza una excepción.
    """
    print(f"Iniciando {name}")
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"Tiempo transcurrido en {name}: {elapsed:.6f} segundos")
