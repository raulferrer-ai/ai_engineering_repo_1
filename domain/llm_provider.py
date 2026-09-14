"""Simulación de una llamada real a un LLM.

Separado de llm_client.py a propósito: el "proveedor" (cómo se hace
la llamada real) debe poder cambiarse sin tocar la orquestación
(rate limit / timeout / retry) que vive en llm_client.py. Mismo
principio que ToolExecutor en protocols.py.
"""

import asyncio
import random


async def fetch_llm_response(
    prompt: str,
    latency_seconds: float = 2.0,
    fail_probability: float = 0.0,
) -> str:
    """Simula una llamada a un LLM.

    fail_probability > 0 fuerza fallos aleatorios: se usa en el
    ejercicio de "Break" para comprobar que retry/rate-limit se
    comportan bien cuando la API real falla de forma intermitente.
    """
    print(f"Llamando al modelo con: {prompt}")
    await asyncio.sleep(latency_seconds)

    if random.random() < fail_probability:
        raise ConnectionError(f"Fallo simulado de red para: {prompt}")

    return f"Respuesta simulada para: {prompt}"
