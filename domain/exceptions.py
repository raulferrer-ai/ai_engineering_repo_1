"""Excepciones propias del dominio.

Se reservan para errores de programación/configuración, no para fallos
esperados y recuperables (esos se modelan con Result[T]).
"""


class RetryExhaustedError(Exception):
    def __init__(self, attempts: int, last_error: Exception) -> None:
        self.attempts = attempts
        self.last_error = last_error
        super().__init__(
            f"Se agotaron los {attempts} intentos. Último error: {last_error}"
        )


class ToolExecutionError(Exception):
    def __init__(self, tool_name: str, reason: str) -> None:
        self.tool_name = tool_name
        self.reason = reason
        super().__init__(f"Tool '{tool_name}' failed: {reason}")
