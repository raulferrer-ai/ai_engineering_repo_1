"""Definición de una tool que un agente puede invocar.

Inmutable a propósito: una vez definida, la configuración de una tool
no debería cambiar durante la ejecución de un agente.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    parameters: dict[str, str] = field(default_factory=dict)
    requires_auth: bool = False
