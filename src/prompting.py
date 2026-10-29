import json

from src.models import FunctionDefinition, PromptInput
from src.file_handler import load_json_file


def build_prompt(
    user_prompt: str,
    functions: list[FunctionDefinition]
) -> str:

    functions_json = json.dumps(
        [function.model_dump() for function in functions],
        indent=2
    )

    return (
        "You are a function calling assistant.\n"
        "Select the most appropriate function for the user request\n"
        "Extract the required arguments from the request.\n"
        "Return only a JSON object with exactly two keys: "
        "'name' and 'parameters'.\n"
        "Use only the functions provided below.\n"
        "Respect the parameter names and types.\n\n"
        f"Available functions: \n{functions_json}\n\n"
        f"User request\n{user_prompt}\n\n"
        "Function call JSON:\n"
    )


if __name__ == "__main__":
    definitions = load_json_file(
        "data/input/functions_definition.json"
    )

    functions = [
        FunctionDefinition.model_validate(item)
        for item in definitions
    ]

    prompts = load_json_file(
        "data/input/function_calling_tests.json"
    )

    first_prompt = PromptInput.model_validate(prompts[0])

    complete_prompt = build_prompt(
        first_prompt.prompt,
        functions
    )

    print(complete_prompt)
