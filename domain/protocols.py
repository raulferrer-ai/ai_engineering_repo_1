"""Protocols del dominio: definen la "forma" que deben tener las
implementaciones, sin imponer herencia (structural typing).
"""

from typing import Protocol


class ToolExecutor(Protocol):
    """Cualquier clase con execute(self, args) -> str conforma a esto,
    sin necesidad de heredar explícitamente.
    """

    def execute(self, args: dict[str, str]) -> str: ...
