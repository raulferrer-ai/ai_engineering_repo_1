"""Context managers del dominio.

timed_block: versión síncrona (Semana 1), para código bloqueante normal.
async_timed_block: versión asíncrona (Semana 2), necesaria para medir
tiempos dentro de funciones `async def` con `async with`. Son dos
protocolos distintos en Python (__enter__/__exit__ vs
__aenter__/__aexit__), por eso hacen falta ambas versiones.
"""

import time
from collections.abc import AsyncGenerator, AsyncIterator, Generator, Iterator
from contextlib import asynccontextmanager, contextmanager


@contextmanager
def timed_block(name: str) -> Generator[None, None, None]:
    print(f"Iniciando {name}")
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"Tiempo transcurrido en {name}: {elapsed:.6f} segundos")


@asynccontextmanager
async def async_timed_block(name: str) -> AsyncGenerator[None, None]:
    print(f"Iniciando {name}")
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"Tiempo transcurrido en {name}: {elapsed:.6f} segundos")
