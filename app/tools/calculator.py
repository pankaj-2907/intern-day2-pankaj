import math
from typing import Dict, Any, Union
from pydantic import BaseModel, Field, field_validator


class CalculatorInput(BaseModel):
    operation: str = Field(..., description="Arithmetic operation: 'add', 'subtract', 'multiply', or 'divide'")
    a: Union[int, float] = Field(..., description="First operand")
    b: Union[int, float] = Field(..., description="Second operand")

    @field_validator("operation")
    @classmethod
    def validate_operation(cls, v: str) -> str:
        valid_ops = {"add", "subtract", "multiply", "divide"}
        normalized = v.strip().lower()
        if normalized not in valid_ops:
            raise ValueError(f"Invalid operation '{v}'. Supported operations: {', '.join(sorted(valid_ops))}")
        return normalized

    @field_validator("a", "b")
    @classmethod
    def validate_finite(cls, v: Union[int, float]) -> Union[int, float]:
        if not math.isfinite(v):
            raise ValueError("Non-finite numeric values (NaN, Infinity) are not allowed.")
        return v


def calculate(operation: str, a: Union[int, float], b: Union[int, float]) -> Dict[str, Any]:
    """
    Performs basic arithmetic operations with strict validation.
    """
    try:
        validated = CalculatorInput(operation=operation, a=a, b=b)
    except Exception as e:
        return {"error": f"Invalid input parameters: {str(e)}", "success": False}

    op = validated.operation
    val_a = validated.a
    val_b = validated.b

    if op == "add":
        res = val_a + val_b
    elif op == "subtract":
        res = val_a - val_b
    elif op == "multiply":
        res = val_a * val_b
    elif op == "divide":
        if val_b == 0:
            return {"error": "Division by zero is not allowed.", "success": False}
        res = val_a / val_b
    else:
        return {"error": f"Unsupported operation: {op}", "success": False}

    if not math.isfinite(res):
        return {"error": "Calculation resulted in a non-finite number.", "success": False}

    if isinstance(res, float) and res.is_integer():
        res = int(res)

    return {"result": res, "success": True}