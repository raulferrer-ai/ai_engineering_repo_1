"""Protocols del dominio: definen la forma requerida, sin imponer
herencia (structural typing)."""

from typing import Protocol


class ToolExecutor(Protocol):
    def execute(self, args: dict[str, str]) -> str: ...
