import pytest

from adapters.calculator_tool import CalculatorTool
from adapters.search_tool import SearchTool
from domain.exceptions import RetryExhaustedError
from domain.result import Result
from domain.retry import run_with_retry
from domain.tool import Tool
from services.tool_registry import ToolRegistry


def test_tool_is_frozen() -> None:
    tool = Tool(name="search", description="busca cosas", requires_auth=True)
    with pytest.raises(Exception):  # FrozenInstanceError
        tool.name = "otro_nombre"  # type: ignore[misc]


def test_result_ok_and_fail() -> None:
    ok = Result.ok(42)
    fail = Result.fail("boom")

    assert ok.is_ok() is True
    assert ok.value == 42
    assert fail.is_ok() is False
    assert fail.error == "boom"


def test_run_with_retry_succeeds_eventually() -> None:
    attempts = {"count": 0}

    def flaky() -> str:
        attempts["count"] += 1
        if attempts["count"] < 2:
            raise ValueError("falla temporal")
        return "ok"

    result = run_with_retry(flaky, max_attempts=3)

    assert result.is_ok()
    assert result.value == "ok"


def test_run_with_retry_raises_when_exhausted() -> None:
    def always_fails() -> str:
        raise ValueError("siempre falla")

    with pytest.raises(RetryExhaustedError) as exc_info:
        run_with_retry(always_fails, max_attempts=2)

    assert exc_info.value.attempts == 2


def test_calculator_tool_add() -> None:
    tool = CalculatorTool()
    result = tool.execute({"operation": "add", "a": "2", "b": "3"})
    assert result == "5"


def test_search_tool_returns_query() -> None:
    tool = SearchTool()
    result = tool.execute({"query": "agentic ai"})
    assert "agentic ai" in result


def test_tool_registry_runs_registered_executor() -> None:
    registry = ToolRegistry()
    registry.register(
        Tool(name="calculator", description="suma y resta"),
        CalculatorTool(),
    )

    result = registry.run("calculator", {"operation": "add", "a": "10", "b": "5"})

    assert result == "15"
    assert len(registry.list_tools()) == 1


def test_tool_registry_raises_for_unknown_tool() -> None:
    registry = ToolRegistry()
    with pytest.raises(KeyError):
        registry.run("no_existe", {})
