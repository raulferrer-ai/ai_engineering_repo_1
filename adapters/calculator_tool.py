"""Implementación concreta de ToolExecutor. No hereda de ToolExecutor
de forma explícita: conforma por estructura (duck typing tipado).
"""


class CalculatorTool:
    def execute(self, args: dict[str, str]) -> str:
        operation = args.get("operation", "")
        a = int(args.get("a", "0"))
        b = int(args.get("b", "0"))

        if operation == "add":
            return str(a + b)
        if operation == "subtract":
            return str(a - b)
        return f"Operación no soportada: {operation}"
