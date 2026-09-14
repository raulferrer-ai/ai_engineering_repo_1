"""Rate limiter basado en espaciado temporal entre llamadas.

Controla la CADENCIA de inicio de llamadas (N por segundo), que es un
concepto distinto de la concurrencia (cuántas a la vez, eso lo haría
un asyncio.Semaphore). Usa asyncio.Lock para que dos coroutines nunca
lean/escriban `_last_call` a la vez -sin el lock, ambas podrían leer
el mismo valor "viejo" y decidir erróneamente que no necesitan
esperar, rompiendo la garantía de tasa.
"""

import asyncio


class RateLimiter:
    def __init__(self, calls_per_second: float) -> None:
        self._interval = 1.0 / calls_per_second
        self._lock = asyncio.Lock()
        self._last_call: float = 0.0

    async def acquire(self) -> None:
        async with self._lock:
            now = asyncio.get_event_loop().time()
            wait = self._last_call + self._interval - now
            if wait > 0:
                await asyncio.sleep(wait)
            self._last_call = asyncio.get_event_loop().time()
