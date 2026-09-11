"""Registro de tools disponibles para un agente.

Depende únicamente del Protocol ToolExecutor, no de las clases
concretas — así puedes registrar cualquier objeto que "tenga la forma"
correcta, sin acoplarte a CalculatorTool/SearchTool.
"""

from domain.protocols import ToolExecutor
from domain.tool import Tool


class ToolRegistry:
    def __init__(self) -> None:
        self._executors: dict[str, ToolExecutor] = {}
        self._definitions: dict[str, Tool] = {}

    def register(self, definition: Tool, executor: ToolExecutor) -> None:
        self._definitions[definition.name] = definition
        self._executors[definition.name] = executor

    def run(self, name: str, args: dict[str, str]) -> str:
        executor = self._executors.get(name)
        if executor is None:
            raise KeyError(f"Tool no registrada: {name}")
        return executor.execute(args)

    def list_tools(self) -> list[Tool]:
        return list(self._definitions.values())
