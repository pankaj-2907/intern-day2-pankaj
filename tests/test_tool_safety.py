import pytest
from pydantic import ValidationError
from app.tools.tools_registry import tool_registry
from app.tools.calculator import CalculatorInput
from app.tools.date_time import DateTimeInput
from app.services.tool_calling_service import ToolCallingService

def test_control_1_and_3_registry_and_invalid_calls():
    """Control 1 & 3: Tool names checked against registry; invalid tool calls do not execute."""
    res = tool_registry.execute_tool("non_existent_tool", {})
    assert res.get("success") is False
    assert "Unknown tool name" in res.get("error", "")

def test_control_2_argument_validation():
    """Control 2: Tool arguments must be validated using Pydantic."""
    with pytest.raises(ValidationError):
        CalculatorInput(operation="invalid_op", a=10, b=5)

def test_control_5_sanitized_errors():
    """Control 5: Errors must not expose stack traces to users."""
    res = tool_registry.execute_tool("calculate", {"operation": "divide", "a": 10, "b": 0})
    assert "error" in res
    assert "Traceback" not in res["error"]
    assert "Division by zero" in res["error"]

def test_control_6_no_arbitrary_code_execution():
    """Control 6 & 9: Calculator and registry prevent arbitrary code/expression evaluation."""
    # Trying to pass code injection into calculator operation or arguments
    with pytest.raises(ValidationError):
        CalculatorInput(operation="__import__('os').system('dir')", a=1, b=1)

def test_control_7_tool_outputs_as_data():
    """Control 7: Tool outputs must be structured dictionaries (data, not instructions)."""
    res = tool_registry.execute_tool("calculate", {"operation": "add", "a": 5, "b": 5})
    assert isinstance(res, dict)
    assert res.get("result") == 10

def test_control_10_malformed_calls_handled_safely():
    """Control 10: Repeated or malformed tool calls handled safely without crashing."""
    res = tool_registry.execute_tool("get_current_datetime", {"timezone": "Invalid/Timezone"})
    assert res.get("success") is False
    assert "error" in res