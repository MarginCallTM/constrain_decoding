from pydantic import BaseModel, ValidationError
from src.file_handler import load_json_file
from typing import Literal


class PromptInput(BaseModel):
    prompt: str


class ParameterDefinition(BaseModel):
    type: Literal[
        "string",
        "number",
        "integer",
        "boolean",
        "array",
        "object",
        "null",
    ]


class FunctionDefinition(BaseModel):
    name: str
    description: str
    parameters: dict[str, ParameterDefinition]
    returns: ParameterDefinition


if __name__ == "__main__":

    definitions = load_json_file(
        "data/input/functions_definition.json"
    )

    validated_definitions = []

    for item in definitions:
        function = FunctionDefinition.model_validate(item)
        validated_definitions.append(function)

    print(f"Functions loaded: {len(validated_definitions)}")

    first_function = validated_definitions[0]

    print(first_function.name)
    print(first_function.parameters["a"].type)
