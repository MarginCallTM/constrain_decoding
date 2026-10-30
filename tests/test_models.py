import pytest
from pydantic import ValidationError

from src.models import (
    PromptInput,
    ParameterDefinition,
    FunctionDefinition,
)


def test_valid_prompt() -> None:
    """Accept a valid prompt"""
    prompt = PromptInput(prompt="Greet Shrek")

    assert prompt.prompt == "Greet Shrek"


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"prompt": None},
        {"prompt": 123},
    ],
)
def test_invalid_prompt(payload: dict) -> None:
    """Reject missing or incorrectly typed prompts."""
    with pytest.raises(ValidationError):
        PromptInput.model_validate(payload)


def test_valid_parameter_definition() -> None:
    """Accept an authorized JSON type."""
    parameter = ParameterDefinition(type="number")

    assert parameter.type == "number"


def test_invalid_parameter_type() -> None:
    """Reject unsupported JSON types."""
    with pytest.raises(ValidationError):
        ParameterDefinition.model_validate(
            {"type": "banana"}
        )


def test_valid_function_definition() -> None:
    """Validate a complete function definition"""
    data = {
        "name": "fn_add_numbers",
        "description": "Add two numbers",
        "parameters": {
            "a": {"type": "number"},
            "b": {"type": "number"},
        },
        "returns": {"type": "number"},
    }

    function = FunctionDefinition.model_validate(data)

    assert function.name == "fn_add_numbers"
    assert function.parameters["a"].type == "number"
    assert function.parameters["b"].type == "number"


def test_missing_function_name() -> None:
    """Reject a function definition whitout a name"""
    data = {
        "description": "Add two numbers",
        "parameters": {
            "a": {"types": "number"},
        },
        "returns": {"types": "number"},
    }

    with pytest.raises(ValidationError):
        FunctionDefinition.model_validate(data)
